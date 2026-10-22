#!/usr/bin/env python3
"""Candidate-only registry preflight. Secrets stay in memory, never diagnostics."""
import base64,hashlib,json,os,re,sys,urllib.request,urllib.error,urllib.parse
SHA='0259b577ef16591d21dd2d93655e68ba21ad1ff0'
REPO='woowtech/amd64-addon-cloudflared-webgui'
TAG='1.0.5-ops03.20261023.0259b577ef16'
EXPECTED={'/run.sh': '9dde80b64ccb7dac2361154355eac66609d7d0c053df2c27943da4e9f744be74', '/etc/s6-overlay/s6-rc.d/prepare/run.sh': 'c94774b2001806fa8f1b68b66c141afec80f4a6e659e2e32dfeec5e5e722f347', '/etc/s6-overlay/s6-rc.d/webgui/run': '0d2431fc0ae95c551c9945aa162537e8a48769fd6f1275aeff5052a0c1ed0a36', '/usr/local/bin/cloudflared-credential-guard': 'b8c09f39941dc292b4b871b51ecae5e80a3765cdf56a5cdfc0124dc3b4b6ebb9', '/opt/webgui/backend/main.py': 'ecca51ea1bd6e2126256e60a0ed3eb67b7d06d9a334c5aed4ac97b470a45663a', '/opt/webgui/backend/metrics.py': '4eaf5dc18928588bb7e78b80757af9d41b990ef7162033d5b97f9c90cd5f9999', '/opt/webgui/backend/models.py': 'f655f5e0a88276e052f1e137bbe2b178808af8caf6a34fc8933ec1f7c4993693', '/opt/webgui/backend/supervisor.py': '5dcdff87f0a1e8ad0af368263d8d24c54924318468009c5ac9537898dcaffc64'}
ACCEPT='application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.index.v1+json'
def fail(code):
 print(json.dumps({'passed':False,'error_code':code}));raise SystemExit(1)
def get(url,headers):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=20) as r:return r.status,r.headers,r.read()
 except urllib.error.HTTPError as e:return e.code,e.headers,b''
def classify(status,mode):
 if mode=='absent':return status==404
 return status==200

def main():
 mode=sys.argv[1]
 if mode=='verify-files':
  actual={line.split()[1]:line.split()[0] for line in open(sys.argv[2]) if line.strip()}
  if actual!=EXPECTED:fail('runtime_source_hash_mismatch')
  print(json.dumps({'runtime_files_match':True,'source_commit':SHA}));return
 if mode not in ['absent','receipt']:fail('unsupported_mode')
 credential=os.environ.get('GH_TOKEN');actor=os.environ.get('GITHUB_ACTOR')
 if not credential or not actor:fail('job_token_missing')
 auth=base64.b64encode((actor+':'+credential).encode()).decode()
 status,_,raw=get('https://ghcr.io/token?'+urllib.parse.urlencode({'service':'ghcr.io','scope':'repository:'+REPO+':pull'}),{'Authorization':'Basic '+auth})
 if status!=200:fail('registry_auth_http_'+str(status))
 token=json.loads(raw).get('token')
 if not token:fail('registry_token_missing')
 status,headers,raw=get('https://ghcr.io/v2/'+REPO+'/manifests/'+TAG,{'Authorization':'Bearer '+token,'Accept':ACCEPT})
 if not classify(status,mode):fail('candidate_manifest_http_'+str(status))
 if mode=='absent':print(json.dumps({'candidate_absent':True,'http_status':status}));return
 digest=headers.get('Docker-Content-Digest','')
 if digest!='sha256:'+hashlib.sha256(raw).hexdigest():fail('manifest_digest_mismatch')
 print(json.dumps({'source_commit':SHA,'version':TAG,'image':'ghcr.io/'+REPO,'manifest_digest':digest,'candidate_ref':'ghcr.io/'+REPO+'@'+digest,'published_tag':TAG,'stable_latest_written':False}))
if __name__=='__main__':
 try:main()
 except Exception as e:fail('operation_failed_'+type(e).__name__)
