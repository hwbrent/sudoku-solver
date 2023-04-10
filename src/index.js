import Solver from './Solver/Solver.js';

const Algorithms = [
    Solver
];

const select = document.querySelector('select');
const startButton = document.querySelector('button');

// Add <option>s to <select>.
for (const algorithm of Algorithms) {
    const option = document.createElement('option');
    option.value = algorithm.name;
    option.innerText = algorithm.name;
    select.appendChild(option);
};

startButton.addEventListener('click', () => {
    const Algo = Algorithms.find(algo => algo.name === select.value);
    const algoInstance = new Algo();
});

// startButton.click();
