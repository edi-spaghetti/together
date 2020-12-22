let o;

function setup() {
    createCanvas(800, 500);

    var x = Math.floor(Math.random() * 800);
    var y = Math.floor(Math.random() * 500);
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
        this.y = y;
        this.size = s;
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
            this.x -= 1;
            console.log('left');
        }
        if (keyIsDown(83)) {
            this.y += 1;
            console.log('down');
        }
        if (keyIsDown(68)) {
            this.x += 1;
            console.log('right');
        }
        if (keyIsDown(87)) {
            this.y -= 1;
            console.log('up');
        }
    }

    draw() {
        fill(255);
        ellipse(this.x, this.y, this.size, this.size);
    }
}
