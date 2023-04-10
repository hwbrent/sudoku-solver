import Cell from '../Cell/Cell.js';

export default class Grid {
    constructor() {
        /** @type {Array<Cell>} */
        this.cells = [];
        this.element = null;

        document.grid = this;
    }

    init() {
        this.addToDOM();
        this.initCells();
        this.generateClues();
    }

    /**
     * @summary Creates element for grid and adds it to DOM.
     * @returns {void} void
     */
    addToDOM() {
        const root = document.getElementById('root');

        this.element = document.createElement('div');
        this.element.id = 'grid';

        root.appendChild(this.element);
    }

    /**
     * @summary Initialises all 81 cells of the sudoku grid.
     * @returns {void} void
     */
    initCells() {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const cell = new Cell(i, j, this);
                this.cells.push(cell);
                cell.addToDOM();
            }
        }
    }

    /**
     * @summary Gets the row with index {@link row_index}.
     * @param {number} row_index - the index of the target row.
     * @returns {Array<Cell>}
     */
    getRow(row_index) {
        const startIndex = row_index * 9;
        const endIndex = startIndex + 9;
        return this.cells.slice(startIndex, endIndex);
    }

    /**
     * @summary Gets the column with index {@link column}.
     * @param {number} column_index - the index of the target column.
     * @returns {Array<Cell>}
     */
    getColumn(column_index) {
        const cells = [];
        for (let i = column_index; i < 81; i += 9) {
            cells.push(this.cells[i]);
        }
        return cells;
    }

    /**
     * @summary Gets the box (i.e. 3x3 sub-grid) containing the {@link Cell}
     *          at {@link row_index} and {@link column_index}.
     * @param {number} row_index - the row index of the cell.
     * @param {number} column_index - the column index of the cell.
     * @returns {Array<Cell>}
     */
    getBox(row_index, column_index) {
        const cells = [];

        const rowLower = Math.floor(row_index / 3) * 3;
        const colLower = Math.floor(column_index / 3) * 3;

        for (let i = rowLower; i < rowLower+3; i++) {
            for (let j = colLower; j < colLower+3; j++) {
                console.debug(i,j);
                cells.push(this.cells[(i*9) + j]);
            }
        }

        return cells;
    }

    generateClues() {
        let cluesPlaced = 0;

        while (cluesPlaced < 17) {
            const minI = 0;
            const maxI = 81;
            const randomIndex = Math.floor(Math.random() * (maxI - minI) + minI);

            const cell = this.cells[randomIndex];

            if (cell.value) {
                continue;
            }

            const minV = 1;
            const maxV = 10;
            const randomValue = Math.floor(Math.random() * (maxV - minV) + minV);

            if (cell.valueIsValid(randomValue)) {
                cell.setClue(randomValue);
                cluesPlaced++;
            }
        }
    }
}
