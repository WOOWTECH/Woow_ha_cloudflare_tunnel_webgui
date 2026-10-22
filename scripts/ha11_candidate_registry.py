#!/usr/bin/env python3
"""Candidate-only registry preflight. Secrets stay in memory, never diagnostics."""
import base64,hashlib,json,os,re,sys,urllib.request,urllib.error,urllib.parse
SHA='e1e14e9ff7d96170b4ea6c266edc01a6746781cf'
REPO='woowtech/amd64-addon-cloudflared-webgui'
TAG='1.0.5-ha11.20261023.e1e14e9ff7d9'
EXPECTED={'/etc/s6-overlay/s6-rc.d/prepare/run.sh': '85ca7807119e0629797a50f91fcf8b09f69049bb2f9662dbf6b50fd792fbb694', '/opt/webgui/backend/main.py': 'ecca51ea1bd6e2126256e60a0ed3eb67b7d06d9a334c5aed4ac97b470a45663a', '/opt/webgui/backend/models.py': 'f655f5e0a88276e052f1e137bbe2b178808af8caf6a34fc8933ec1f7c4993693', '/opt/webgui/backend/supervisor.py': '5dcdff87f0a1e8ad0af368263d8d24c54924318468009c5ac9537898dcaffc64', '/run.sh': 'eb8fcaedb214e39b58918c7036ef0e5ce139dc68b1e576d8331339778cd12c77', '/opt/webgui/backend/metrics.py': '4eaf5dc18928588bb7e78b80757af9d41b990ef7162033d5b97f9c90cd5f9999'}
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
