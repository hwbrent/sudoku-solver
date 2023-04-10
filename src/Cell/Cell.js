export default class Cell {
    constructor(row, col, grid) {
        this.element = null;
        this.span = null;

        this.row = row;
        this.col = col;
        this.grid = grid;
        this._value = null;
    }

    addToDOM() {
        this.element = document.createElement('div');
        this.element.classList.add('cell');
        // this.element.dataset['row'] = row;
        // this.element.dataset['col'] = col;

        this.span = document.createElement('span');
        this.element.appendChild(this.span);

        this.grid.element.appendChild(this.element);
    }

    get value() {
        return this._value;
    }
    set value(newValue) {
        this._value = newValue;

        this.span.innerText = this._value;
    }
}
