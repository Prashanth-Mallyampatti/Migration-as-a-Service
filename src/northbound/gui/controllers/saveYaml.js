const yaml = require('json-to-pretty-yaml');
const fse = require('fs-extra');

let save = (object, username, filename)=>{
    yamlString = yaml.stringify(object);
    let name = `output/${filename}.yml`;
    console.log(name,yamlString);
    fse.outputFileSync(name, yamlString);
}

module.exports.save = save;
