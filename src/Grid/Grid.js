import Cell from '../Cell/Cell.js';

export default class Grid {
    constructor() {
        this.cells = [];
        this.element = null;

        document.grid = this;
    }

    init() {
        this.addToDOM();
        this.initCells();
    }

    addToDOM() {
        const root = document.getElementById('root');

        this.element = document.createElement('div');
        this.element.id = 'grid';

        root.appendChild(this.element);
    }

    initCells() {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const cell = new Cell(i, j, this);
                this.cells.push(cell);
                cell.addToDOM();
            }
        }
    }

    getRow(row_index) {
        const startIndex = row_index * 9;
        const endIndex = startIndex + 9;
        return this.cells.slice(startIndex, endIndex);
    }

    getColumn(column_index) {
        const cells = [];
        for (let i = column_index; i < 81; i += 9) {
            cells.push(this.cells[i]);
        }
        return cells;
    }

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
}
