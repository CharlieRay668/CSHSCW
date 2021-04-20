
// setup canvas
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

const width = canvas.width = window.innerWidth;
const height = canvas.height = window.innerHeight;

// function to generate random number
function random(min, max, decimal) {
    const num = Math.floor(Math.random() * (max - min + 1)) + min;
    const mult = decimal*10
    if (mult >= 1) {
        return (num*mult)/mult
    }
    return num;
}

function degToRad(degrees) {
    return degrees * Math.PI / 180;
};

function Nest(x, y, r, foodCount) {
    this.x = x
    this.y = y
    this.r = r
    this.foodCount = foodCount
}

Nest.prototype.draw = function() {
    ctx.beginPath();
    ctx.fillStyle = 'rgb(255,0,0)';
    ctx.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
    ctx.fill();
};

function Vector(magnitude, direction){
    this.magnitude = magnitude
    this.direction = direction
}

Vector.prototype.getX = function() {
    return this.magnitude*Math.cos(degToRad(this.direction))
}
Vector.prototype.getY = function() {
    return this.magnitude*Math.sin(degToRad(this.direction))
}
Vector.prototype.flipX = function() {
    this.direction = (180-this.direction)
}
Vector.prototype.flipY = function() {
    this.direction = (360-this.direction)
}

function Pheremone(x, y, type, direction) {
    this.x = x;
    this.y = y;
    this.type = type;
    this.direction = direction;
    this.clock = 0;
}

Pheremone.prototype.draw = function() {
    if (this.clock < 0) {
        ctx.beginPath();
        if (this.type == "FOOD") {
            ctx.fillStyle = 'rgb(255,0,0)';
        } else {
            ctx.fillStyle = 'rgb(0,0,255)';
        }
        ctx.arc(this.x, this.y, 2, 0, 2 * Math.PI);
        ctx.fill();
        x = this.x+this.direction.getX();
        y = this.y+this.direction.getY();
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(x, y);
        ctx.lineTo(x+4, y);
        ctx.lineTo(this.x, this.y);
        ctx.fill();
        
    }
};

Pheremone.prototype.update = function() {
    if (this.clock > 400) {
        const index = pheremones.indexOf(this);
        if (index > -1) {
            pheremones.splice(index, 1);
        }
    }
    this.clock++;
}

function Food(x, y, foodAmount) {
    this.x = x;
    this.y = y;
    this.foodAmount = foodAmount;
};

Food.prototype.draw = function() {
    ctx.beginPath();
    ctx.fillStyle = 'rgb(0,255,0)';
    ctx.arc(this.x, this.y, 10, 0, 2 * Math.PI);
    ctx.fill();
};

// define Ball constructor
function Ant(x, y, velocity, color, size) {
    this.x = x;
    this.y = y;
    this.velocity = velocity;
    this.color = color;
    this.size = size;
    this.clock = 0;
    this.hasFood = false;
}

// define ball draw method

Ant.prototype.draw = function() {
    ctx.beginPath();
    ctx.fillStyle = this.color;
    ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
    ctx.fill();
};

// define ball update method

Ant.prototype.update = function() {
    this.velocity.direction += random(-10, 10, 0)
    const dx = this.x - width/2;
    const dy = this.y - height/2;
    const distance = Math.sqrt(dx * dx + dy * dy);
    if (distance < this.size + 40) {
        this.hasFood = false;
        nest.foodCount++;
    }
    if((this.x + this.size) >= width) {
        this.velocity.flipX()
    }

    if((this.x - this.size) <= 0) {
        this.velocity.flipX()
    }

    if((this.y + this.size) >= height) {
        this.velocity.flipY()
    }

    if((this.y - this.size) <= 0) {
        this.velocity.flipY()
    }
    if(this.clock > 10) {
        
        //var angleDeg = Math.atan2(0, 0) * 180 / Math.PI;
        if (this.hasFood) {
            pheremones.push(new Pheremone(this.x, this.y, "FOOD", new Vector(10, this.velocity.direction-180)));
        } else {
            var angleDeg = Math.atan2(height/2 - this.y, width/2 - this.x) * 180 / Math.PI;
            pheremones.push(new Pheremone(this.x, this.y, "HOME", new Vector(10, angleDeg)));
        }
        this.clock = 0;
    }
    this.clock++;
    this.x += this.velocity.getX();
    this.y += this.velocity.getY();
};

// define ball collision detection

Ant.prototype.collisionDetectAnts = function() {
    for(let j = 0; j < ants.length; j++) {
        if(!(this === ants[j])) {
        const dx = this.x - ants[j].x;
        const dy = this.y - ants[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < this.size + ants[j].size) {
                ants[j].color = this.color = 'rgb(' + random(0,255,0) + ',' + random(0,255,0) + ',' + random(0,255,0) +')';
            }
        }
    }
};

Ant.prototype.collisionDetectFood = function() {
    for(let j = 0; j < food.length; j++) {
        const dx = this.x - food[j].x;
        const dy = this.y - food[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.size + 20) {
            this.hasFood = true;
        }
    }
};
Ant.prototype.collisionDetectPheremone = function() {
    for(let j = 0; j < pheremones.length; j++) {
        if ((pheremones[j].type == "FOOD" && !this.hasFood) || (pheremones[j].type == "HOME" && this.hasFood)) {
            const dx = this.x - pheremones[j].x;
            const dy = this.y - pheremones[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < this.size + 30) {
                this.velocity.direction = pheremones[j].direction.direction
            }
        }
    }
};

let nest = new Nest(width/2, height/2, 40);

let ants = [];
let pheremones = [];

while(ants.length < 100) {
    const size = 5;
    let ant = new Ant(width/2,height/2,new Vector(3, random(0,360,10)),'rgb(0,0,255)',size);
    ants.push(ant);
}

let food = [];
while(food.length < 20){
    let foodSpot = new Food(random(30, width-30, 0), random(30, height-30, 0), 100)
    food.push(foodSpot)
}

// define loop that keeps drawing the scene constantly

function loop() {
    ctx.fillStyle = 'rgba(0,0,0,0.25)';
    ctx.fillRect(0,0,width,height);
    nest.draw();
    for(let i = 0; i < ants.length; i++) {
        ants[i].draw();
        ants[i].update();
        ants[i].collisionDetectAnts();
        ants[i].collisionDetectFood();
        ants[i].collisionDetectPheremone();
    }
    for(let i = 0; i < food.length; i++) {
        food[i].draw()
    }
    for(let i = 0; i < pheremones.length; i++) {
        pheremones[i].draw()
        pheremones[i].update()
    }
    requestAnimationFrame(loop);
}

loop();