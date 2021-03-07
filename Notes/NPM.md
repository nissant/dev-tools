# Useful npm Commands
rm -rf node_modules && npm install

npm uninstall -S <pkg>

npm install -S <pkg>@latest

npx depcheck

// Finding a pacakge in npm
npm list <pkg> 

# Setting Up Node.js Env
1.	Download and install latest LTS Node.JS. (Node 12+ increases the heap sizes automatically, that is why you saw memory issues on Node 10 when running Plotly)
2.	$ cd ..\gitlab\dashboard-frontend
3.	$ npm cache clean --force
4.	Delete node_modules folder and package-lock.json in frondend repo.
5.	Pull latest frontend GIT repo.
6.	$ npm install
7.	$ npm start

# Building Production Build (according to package.json config)
npm run build
