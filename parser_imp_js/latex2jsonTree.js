const latexmath = require('math-expressions')
var argv = require('minimist')(process.argv.slice(2))
console.dir(argv);
const expression = argv['e']
const outputfile = argv['o']

var node = latexmath.fromLaTeX( 'a_t=\sum_{i=1}^t p_i' )
console.log( node.toString())
// load math.js (using node.js)
//const node = math.parse( expression )
// var counter = 0
// node.traverse(function (node, path, parent) {
//     node.id = counter
//     counter = counter + 1
// })

// const res = {}

// node.traverse(function (node, path, parent) {
//      console.log("================")
//      const njson = node.toJSON()
//      njson.id = node.id

//      if(parent != null ){
//         // console.log(parent.toJSON())
//         // pjson = parent.toJSON()
//         njson.parent_id = parent.id
//      } else {
//         //console.log(parent)
//         njson.parent_id = -1
//      }
//      //console.log(node.toJSON())
//      console.log(njson)
//      res[njson.id] = njson
// //     console.log(path)
// })
// const latex = node.toTex()

// console.log(node.toTex())

// var jsonContent = JSON.stringify(res)
// // file system module to perform file operations
// const fs = require('fs')
// fs.writeFile(outputfile, jsonContent, 'utf8', function (err) {
//     if (err) {
//         console.log("An error occured while writing JSON Object to File.");
//         return console.log(err);
//     }

//     console.log("JSON file has been saved.");
// });