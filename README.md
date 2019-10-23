# scobra

Scobra is a supplementary package for COBRApy designed by Maurice Cheung used by the Yale-NUS Computational and Systems Biology team. This version is specifically for Python 3.

To install scobra, run this line:

pip install scobra -r requirements.txt

## Accessing scobra through the server using Jupyter Notebook 
0. Make sure [Jupyter](http://jupyter.org/install) is installed in your local machine <br/>
1. Connect to the server using your account <br/>
```
ssh your_username@172.25.20.52
```
2. Activate Jupyter Notebook in the server<br/>
``` 
jupyter notebook --no-browser --port=8889
```
3. Connect your local machine to the remote jupyter notebook session <br/>
```
ssh -N -f -L localhost:8888:localhost:8889 your_username@172.25.20.52
```
4. Open your browser and access <br/>
```
localhost:8888
```
5. If this is the first time your browser opens the session, you may need to provide a token. The token is displayed in your terminal running jupyter notebook remotely. It should look something like this: <br/>
```
Copy/paste this URL into your browser when you connect for the first time, to login with a token:
        http://localhost:8889/?token=779c5074bbe9c26338a8760875e0c0ba3f77294201f61353
```
Copy everything after `http://localhost:8889/?token=` to the box provided and login. <br/>

## Copying files to and from server 
To copy files from local machine to server, run: 
```
scp path/to/local/file username@172.25.20.52:path/to/remote/directory
```

To copy files from server to local machine, run: 
```
scp username@172.25.20.52:path/to/remote/directory path/to/local/file
```
Note: to copy folders, use `scp -r` instead of `scp` 