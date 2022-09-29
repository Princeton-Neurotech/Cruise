const { execSync } = require("child_process");

// FILENAMES
const manifestFileName = "manifest.json";

// DIRECTORIES
const buildDir = "./build/";
const extensionDir = "./public/";
const outputs = "./";

// OUTPUTS
const chromeOutput = "chrome-new-and-improved.zip";

console.log("Building Extension Packages");

console.log("***COPYING MANIFEST FILE***\n\n");
execSync(
  `cp ${extensionDir}${manifestFileName} ${buildDir}${manifestFileName}`
);

execSync(`zip -r ${outputs}${chromeOutput} ${buildDir}`);
console.log("***CHROME BUILT SUCCESSFULLY***\n\n");

execSync(`web-ext build -s ${buildDir} -a ${outputs} --overwrite-dest`);
console.log("***FIREFOX BUILT SUCCESSFULLY***");