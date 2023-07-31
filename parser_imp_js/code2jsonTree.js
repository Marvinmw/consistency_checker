const math = require('mathjs')
const latexmath = require('math-expressions')

var argv = require('minimist')(process.argv.slice(2))
console.dir(argv);


const expression = argv['e']
const outputfile = argv['o']

// load math.js (using node.js)
const node = math.parse( expression )
try {
    const orgnode = math.parse( expression )
    const node = math.simplify(orgnode) 
  } catch (error) {
    const node = math.parse( expression )
    // Expected output: ReferenceError: nonExistentFunction is not defined
    // (Note: the exact output may be browser-dependent)
  }
  
var counter = 0
node.traverse(function (node, path, parent) {
    node.id = counter
    counter = counter + 1
})

const nodes_dic = {}

node.traverse(function (node, path, parent) {
    // console.log("================")
     const njson = node.toJSON()
     // console.log(node.toString())
     text = node.toString()
     njson.id = node.id
     njson.text = text
     if(parent != null ){
        // console.log(parent.toJSON())
        // pjson = parent.toJSON()
        njson.parent_id = parent.id
     } else {
        //console.log(parent)
        njson.parent_id = -1
     }
     //  console.log(node.toJSON())
     //  console.log(njson)
     nodes_dic[njson.id] = njson
//     console.log(path)
})
const latex = node.toTex()
const res = {}
res['nodes'] = nodes_dic
res['latex'] = latex
res['expression'] = expression
res['simplify'] = node.toString()
//console.log("node.toTex()")
//console.log(node.toTex())
// var f = latexmath.fromLaTeX(latex)
// console.log("latexmath.fromTeX()")
// console.log(f)
var jsonContent = JSON.stringify(res)
console.log(jsonContent)
// file system module to perform file operations
const fs = require('fs')
fs.writeFile(outputfile, jsonContent, 'utf8', function (err) {
    if (err) {
        console.log("An error occured while writing JSON Object to File.");
        return console.log(err);
    }

    console.log("JSON file has been saved.");
});