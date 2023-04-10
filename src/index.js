import Solver from './Solver/Solver.js';

const Algorithms = [
    Solver
];

/**
 * @summary Adds a `<select>` element to the page which allows the user to
 * select an algorithm with which to solve the sudoku.
 */
function populateSelect() {
    const select = document.querySelector('select');

    // Add <option>s to <select>.
    for (const algorithm of Algorithms) {
        const option = document.createElement('option');
        option.value = algorithm.name;
        option.innerText = algorithm.name;
        select.appendChild(option);
    };
}

const startButton = document.querySelector('button');
startButton.addEventListener('click', () => {
    const select = document.querySelector('select');
    const Algo = Algorithms.find(algo => algo.name === select.value);

    const algoInstance = new Algo();
});

populateSelect()

// startButton.click();
