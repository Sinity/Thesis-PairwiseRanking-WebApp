To run frontend & backend on NixOS (assuming git is installed):
```bash
 $ git clone https://github.com/Sinity/pwrank.git
 $ cd pwrank
 $ nix-shell
   # necessary only once after cloning, unless dependencies change
 $ (cd frontend && npm install) 
 $ (cd frontend && npm run serve) &
 $ python backend/webrankit/app.py
```
