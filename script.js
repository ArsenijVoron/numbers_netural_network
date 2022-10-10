let canv = document.getElementById('canvas');
let ctx = canv.getContext('2d');
ctx.lineWidth = 36 * 2;
let text = document.getElementById('text');
const step = canv.height / 30
let lineWidth = 0;
let data;
let canWrite = true;
let mousedown = false;
let readyAllow = false;
let numberCount = 1;
let numarray = [];
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
    '9': []
};


document.getElementById('ready').onclick = () =>
{
    if(readyAllow)
    {
        if(numberCount < 100)
            text.textContent = `рисуй ${Math.floor((numberCount) / 10)} ${(Math.floor(numberCount / 10) + 1) * 10 - numberCount} раз`;
        let arr = [];
        let _draw = [];
        for(let x = 0; x < canv.width; x += step)
        {
            for(let y = 0; y < canv.height; y += step)
            {
                let pixelCount = 0;
                data = ctx.getImageData(y, x, step, step);
                for(let i = 0; i < data.data.length; i++)
                {
                    if(data.data[i] !== 0)
                    {
                        pixelCount ++;
                    }
                }
                if(pixelCount > 0)
                {
                    _draw.push([y, x, step, step]);
                }
                arr.push(pixelCount > 0 ? 1 : 0);
            }
        }
        console.log(arr)
        dataSet[Math.floor((numberCount - 1) / 10)].push(arr);
        for(_d in _draw)
        {
            drawCell(_draw[_d][0], _draw[_d][1], _draw[_d][2], _draw[_d][3]);
        }
        drowGrid();
        if(numberCount == 100) 
        {
            text.textContent = "готово";
            const blob = new Blob([JSON.stringify(dataSet)], {type: 'application/json'});
            saveAs(blob, "dataSet.json");
        }    
        readyAllow = false;
        canWrite = false;
        numberCount ++;
        document.getElementById('ready').textContent = 'следующая';
    }
    else
    {
        document.getElementById('ready').textContent = 'готово';
        clear();
    }
}

function drawCell(x, y, w, h)
{
    clear();
    lineWidth = ctx.lineWidth;
    ctx.rect(x, y, w, h);
    ctx.fill();
    ctx.lineWidth = lineWidth;

}


function drowGrid()
{
    lineWidth = ctx.lineWidth;
    ctx.lineWidth = 1;
    for(let x = step; x < canv.height; x += step)
    {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canv.height);
        ctx.stroke();
    }

    for(let y = step; y < canv.width; y += step)
    {
        ctx.moveTo(0, y);
        ctx.lineTo(canv.width, y);
        ctx.stroke();
    }
    ctx.lineWidth = lineWidth;
}   

function clear ()
{
    canWrite = true;
    ctx.clearRect(0, 0, canv.width, canv.height);
}


document.getElementById('clear').onclick = () =>
{
    if(document.getElementById('ready').textContent == 'следующая')
        document.getElementById('ready').textContent = 'готово'
    clear();
    readyAllow = false;
}
canv.addEventListener('mousedown', () =>
{
    mousedown = true;
    ctx.beginPath();
})

canv.addEventListener('mouseout', () =>
{
    mousedown = false;
    ctx.beginPath();
})

canv.addEventListener('mouseup', () =>
{
    mousedown = false;
    ctx.beginPath();
})

canv.addEventListener('mousemove', (e) =>
{
    if (mousedown)
    {
        if(canWrite)
        {
            ctx.lineTo(e.offsetX, e.offsetY);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(e.offsetX, e.offsetY, 36, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.lineTo(e.offsetX, e.offsetY);
            readyAllow = true;
        }
    }
})