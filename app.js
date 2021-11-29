const express = require('express');
const app = express();
const { spawn } = require('child_process');

const port = process.env.PORT || 3000;

app.listen(port, function () {
  console.log('web is connected to server listening');
});

// necessary express middleware
app.use(express.static('public'));
app.use(express.urlencoded({ extended: false }));
app.set('view engine', 'ejs'); // register view engine with node express - the default folder for view engine files are "views" (we already have)

//----------------------------------------------------------------------------------------------------------------------------------------------------------------

// get home page route
app.get('/', function (req, res) {
  // res.sendFile(__dirname + "/views/index.html"); using
  res.render('index');
});

// get user input page route dynamically using routing params
app.get('/userinput/:careerPath', function (req, res) {
  const careerPathSelection = req.params.careerPath;
  let careerPathName;
  if (careerPathSelection === 'da') {
    careerPathName = 'data analyst';
  } else if (careerPathSelection === 'ds') {
    careerPathName = 'data scientist';
  } else {
    careerPathName = 'machine learning engineer';
  }
  res.render('user_input', { careerPathName });
});

// get schedule result page dynamically with ejs coding
app.post('/result', function (req, res) {
  const daTargetCompany = ['Accenture', 'iTechArt', 'Tableau', 'IBM', 'RBC', 'Deloitte', 'TD', 'Citi', 'EY'];
  const dsAndMleTargetCompany = ['RBC', 'Huawei', 'Qualcomm', 'AltaML', 'Bell Canada', 'Deloitte', 'AMD'];
  const { careerPath, terms, skillsTree } = req.body;

  let careerPathNew = careerPath;
  if (careerPathNew === 'machine learning engineer') {
    careerPathNew = 'machine learning';
  }
  const skillList = skillsTree
    .toLowerCase()
    .slice(0, skillsTree.length - 2)
    .split(', ');

  const paramFile = 'mie1624Proj_part4_data.csv';
  const paramDict = {
    'Career Path Choice': careerPathNew,
    'Skills Tree': skillList,
    'Program Length': Number(terms),
  };
  const pyAlgoProg = spawn('python', ['algo.py', paramFile, JSON.stringify(paramDict)]);
  pyAlgoProg.stdout.on('data', function (data) {
    const result = eval(data.toString());
    res.render('result', {
      result,
      daTargetCompany,
      dsAndMleTargetCompany,
      careerPath,
    });
  });
});
