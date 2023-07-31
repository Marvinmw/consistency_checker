#node code2jsonTree.js -e "delta =  mul(log_2(globalRank)-10, TERM_AMPLIFIER)"  -o code2jsonTree_demo.json
# (T*log(cR-cu, 2))*AMP(s)*(EAA(cR) + 1))
node code2jsonTree.js -e "!a"  -o code2jsonTree_demo.json

{"nodes":{"0":{"mathjs":"FunctionNode","fn":{"mathjs":"AccessorNode","object":{"mathjs":"SymbolNode","name":"a"},"index":{"mathjs":"IndexNode","dimensions":[{"mathjs":"ConstantNode","value":"b"}],"dotNotation":true}},"args":[{"mathjs":"OperatorNode","op":"+","fn":"add","args":[{"mathjs":"SymbolNode","name":"h"},{"mathjs":"SymbolNode","name":"c"}],"implicit":false,"isPercentage":false}],"id":0,"text":"a.b(h + c)","parent_id":-1},
"1":{"mathjs":"AccessorNode","object":{"mathjs":"SymbolNode","name":"a"},"index":{"mathjs":"IndexNode","dimensions":[{"mathjs":"ConstantNode","value":"b"}],"dotNotation":true},"id":1,"text":"a.b","parent_id":0},
"2":{"mathjs":"SymbolNode","name":"a","id":2,"text":"a","parent_id":1}
,"3":{"mathjs":"IndexNode","dimensions":[{"mathjs":"ConstantNode","value":"b"}],
"dotNotation":true,"id":3,"text":".b","parent_id":1},
"4":{"mathjs":"ConstantNode","value":"b","id":4,"text":"\"b\"","parent_id":3},
"5":{"mathjs":"OperatorNode","op":"+","fn":"add","args":[{"mathjs":"SymbolNode","name":"h"},{"mathjs":"SymbolNode","name":"c"}],"implicit":false,"isPercentage":false,"id":5,"text":"h + c","parent_id":0},"6":{"mathjs":"SymbolNode","name":"h","id":6,"text":"h","parent_id":5},"7":{"mathjs":"SymbolNode","name":"c","id":7,"text":"c","parent_id":5}},"latex":"\\mathrm{b}\\left(\\mathrm{h}+ c\\right)"}