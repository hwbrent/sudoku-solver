import { Solver } from './Solver/Solver.js';

function start(event) {
    event.target.remove();

    const solver = new Solver();
}

const startButton = document.querySelector('button');
startButton.addEventListener('click', start);
