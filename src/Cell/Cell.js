import Grid from '../Grid/Grid.js';

export default class Cell {
    constructor(row, col, grid) {
        this.element = null;
        this.span = null;

        this.row = row;
        this.col = col;

        /** @type {Grid} */
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

    valueIsValid(val) {
        const value = val ?? this.value;

        const removeThis = (arr) => arr.splice(arr.indexOf(this), 1);
        const mapValues = (arr) => arr.map((cell) => cell.value);

        let thisRow = this.grid.getRow(this.row);
        let thisColumn = this.grid.getColumn(this.col);
        let thisBox = this.grid.getColumn(this.row, this.col);

        removeThis(thisRow);
        removeThis(thisColumn);
        removeThis(thisBox);

        thisRow = mapValues(thisRow);
        thisColumn = mapValues(thisColumn);
        thisBox = mapValues(thisBox);

        return (
            !thisRow.includes(value) &&
            !thisColumn.includes(value) &&
            !thisBox.includes(value)
        )
    }

    setClue(value) {
        this.isClue = true;
        this.value = value;
        this.element.style.setProperty('background-color', '#bfbfbf');
    }
}
