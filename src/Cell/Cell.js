export default class Cell {
    constructor(row, col, grid) {
        this.row = row;
        this.col = col;
        this.grid = grid;
    }

    addToDOM() {
        this.element = document.createElement('div');
        this.element.classList.add('cell');
        // this.element.dataset['row'] = row;
        // this.element.dataset['col'] = col;

        this.grid.element.appendChild(this.element);
    }
}
