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
}
