// let results = ["My name is lola bitch what are you talking about","never love you like i loved ya","never cheat never lied","never put no one above ya","i gave you space and time","do you stay up late","just so you can dream"]
let results = "my name is madhuri";
let term = "madhuri";

// for(let i = 0; i < results.length; i++){
//     results[i].replace(new RegExp(term, "gi"), (match) => `<mark>${match}</mark>`);
//
// }
results.replace(new RegExp(term, "gi"), (match) => `<mark>${match}</mark>`);
console.log(results);

var str = "Hello world, welcome to the universe.";
var n = str.includes("world");
if(n){
    console.log("helloooo") }
    document.write(n.fontcolor( "blue" ));}