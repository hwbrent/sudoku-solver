export default class Cell {
    constructor(row, col, grid) {
        this.element = null;
        this.span = null;

        this.row = row;
        this.col = col;
        this.grid = grid;
    }

    addToDOM() {
        this.element = document.createElement('div');
        this.element.classList.add('cell');
        // this.element.dataset['row'] = row;
        // this.element.dataset['col'] = col;

        this.span = document.createElement('span');
        this.span.classList.add('cell-value');
        this.element.appendChild(this.span);

        this.grid.element.appendChild(this.element);
    }
}
