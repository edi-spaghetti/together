let o;
let socket = io();
socket.on('connect', function() {
    socket.emit('start_game', {data: 'I\'m connected!'});
});

let CWIDTH = 800;
let CHEIGHT = 500;

function setup() {
    createCanvas(CWIDTH, CHEIGHT);

    var x = Math.random();
    var y = Math.random();
    console.log(x, y);

    o = new Mover(x, y, 20);
}

function draw() {
    background(151);
    o.update();
    o.draw();
}

class Mover {

    constructor(x, y, s) {
        this.x = x;
        this.cx = Math.floor(x * CWIDTH);
        this.y = y;
        this.cy = Math.floor(y * CHEIGHT);
        this.size = s;
        socket.emit(
            'add_thrall', {x: this.x, y: this.y, size: this.size}
        )
        console.log('initialised with', x, y, s);
    }

    update() {
        this.checkKeys();
    }

    checkKeys() {

        //KeyCode: 65
        //Key: a
        //KeyCode: 83
        //Key: s
        //KeyCode: 68
        //Key: d
        //KeyCode: 87
        //Key: w

        if (keyIsDown(65)) {
            this.cx -= 1;
//            console.log('left');
        }
        if (keyIsDown(83)) {
            this.cy += 1;
//            console.log('down');
        }
        if (keyIsDown(68)) {
            this.cx += 1;
//            console.log('right');
        }
        if (keyIsDown(87)) {
            this.cy -= 1;
//            console.log('up');
        }
    }

    draw() {
        fill(255);
        ellipse(this.cx, this.cy, this.size, this.size);
    }
}
