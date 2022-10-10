let fs = require('fs');
let dir = fs.readdirSync('./files');
let dataSet = {
    '0': [],
    '1': [],
    '2': [],
    '3': [],
    '4': [],
    '5': [],
    '6': [],
    '7': [],
    '8': [],
    '9' : []
}

for (let i = 0; i < dir.length; i++)
{
    let fileData = JSON.parse(fs.readFileSync(`./files/${dir[i]}`, 'utf-8'))
    for(let j = 0; j < 10; j++)
        for(let k = 0; k < 10; k++)
            dataSet[String(j)].push(fileData[String(j)][k])
}
fs.writeFileSync('dataSet.json', JSON.stringify(dataSet))