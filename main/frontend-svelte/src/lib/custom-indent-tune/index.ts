// $lib/custom-indent-tune/index.ts

interface EditorJSAPI {
    // blocks: {
    //     update: (blockId: string, data: any) => void; // We might not need this if tune saves correctly
    // };
    // If you need to notify the editor for its internal onChange, you might use other API parts
    // or rely on the block's input event dispatching.
}

interface BlockAPI {
    id: string;
    data: any; // The block tool's data (e.g., {text: '...'} for paragraph)
    holder: HTMLElement; // The main wrapper for the block
    readonly name: string;
}

interface IndentTuneConfig {
    defaultIndentSize?: number;
    maxIndentLevel?: number;
}

// This is the TUNE'S data structure
interface TuneData {
    indentLevel: number; // Ensure it's always a number
}

export default class IndentTune {
    private api: EditorJSAPI;
    private block: BlockAPI;
    private config: IndentTuneConfig;

    // This will hold the TUNE'S data, e.g., { indentLevel: 0 }
    // It's initialized in the constructor.
    private tuneData: TuneData;

    private defaultIndentSize: number;
    private maxIndentLevel: number;
    private minIndentLevel: number;

    private _CSS: {
        wrapper: string;
        button: string;
        buttonLeft: string;
        buttonRight: string;
        buttonActive: string;
        buttonDisabled: string;
    };
    private decreaseButton!: HTMLButtonElement;
    private increaseButton!: HTMLButtonElement;

    static get isTune(): boolean {
        return true;
    }

    constructor({
                    api,
                    data, // This `data` is the TUNE'S previously saved data
                    config,
                    block
                }: {
        api: EditorJSAPI;
        data?: Partial<TuneData>; // Make it optional and allow partial data
        config?: IndentTuneConfig;
        block: BlockAPI;
    }) {
        this.api = api;
        this.block = block;
        this.config = config || {};
        // console.log(this.api)
        // console.log(this.block.holder)
        // console.log(`IndentTune CONSTRUCTOR for block "${block?.name}" (ID: ${block?.id}). Holder available:`, !!block?.holder, "Block Data:", block?.data);
        // Initialize tuneData:
        // If `data` is provided and has `indentLevel`, use it. Otherwise, default to 0.
        this.tuneData = {
            indentLevel: (data && typeof data.indentLevel === 'number') ? data.indentLevel : 0
        };
        // console.log(`IndentTune constructor for block ${block.name} (${block.id}). Initial tuneData:`, this.tuneData, "Received data:", data);


        this.defaultIndentSize = this.config.defaultIndentSize || 20;
        this.maxIndentLevel = this.config.maxIndentLevel || 5;
        this.minIndentLevel = 0;

        this._CSS = {
            wrapper: 'ce-indent-tune',
            button: 'ce-indent-tune__button',
            buttonLeft: 'ce-indent-tune__button--left',
            buttonRight: 'ce-indent-tune__button--right',
            buttonActive: 'ce-indent-tune__button--active',
            buttonDisabled: 'ce-indent-tune__button--disabled'
        };
    }

    render(): HTMLDivElement {
        const wrapper = document.createElement('div');
        wrapper.classList.add(this._CSS.wrapper);

        this.decreaseButton = document.createElement('button');
        this.decreaseButton.type = 'button';
        this.decreaseButton.classList.add(this._CSS.button, this._CSS.buttonLeft);
        this.decreaseButton.innerHTML = this._createLeftIcon();
        this.decreaseButton.title = 'Decrease indent';
        this.decreaseButton.addEventListener('click', () => this._decreaseIndent());

        this.increaseButton = document.createElement('button');
        this.increaseButton.type = 'button';
        this.increaseButton.classList.add(this._CSS.button, this._CSS.buttonRight);
        this.increaseButton.innerHTML = this._createRightIcon();
        this.increaseButton.title = 'Increase indent';
        this.increaseButton.addEventListener('click', () => this._increaseIndent());

        wrapper.appendChild(this.decreaseButton);
        wrapper.appendChild(this.increaseButton);

        this._updateButtonStates();
        this._applyIndentStyles(this.tuneData.indentLevel); // Apply initial style
        return wrapper;
    }

    private _createLeftIcon(): string {
        return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M3 8L7 4V12L3 8Z"/><path d="M7 7H13V9H7V7Z"/></svg>';
    }

    private _createRightIcon(): string {
        return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M13 8L9 12V4L13 8Z"/><path d="M9 7H3V9H9V7Z"/></svg>';
    }

    private _increaseIndent(): void {
        if (this.tuneData.indentLevel < this.maxIndentLevel) {
            this.tuneData.indentLevel++;
            this._applyIndentStyles(this.tuneData.indentLevel);
            this._updateButtonStates();
            this._dispatchBlockChanged();
        }
    }

    private _decreaseIndent(): void {
        if (this.tuneData.indentLevel > this.minIndentLevel) {
            this.tuneData.indentLevel--;
            this._applyIndentStyles(this.tuneData.indentLevel);
            this._updateButtonStates();
            this._dispatchBlockChanged();
        }
    }

    private _getCurrentIndentLevel(): number {
        // Now reads directly from the tune's managed state
        return this.tuneData.indentLevel;
    }

    // No _setIndentLevel needed as we directly modify this.tuneData.indentLevel

    private _getTargetStylingElement(): HTMLElement | null {
        return this.block.holder.querySelector('.ce-block__content');
    }

    private _applyIndentStyles(level: number): void {
        const elementToStyle = this._getTargetStylingElement() || this.block.holder;
        const indentSize = level * this.defaultIndentSize;
        elementToStyle.style.paddingLeft = indentSize > 0 ? `${indentSize}px` : '';
        // console.log(`Applied paddingLeft ${elementToStyle.style.paddingLeft || '0px'} to`, elementToStyle, `for block ${this.block.id}`);
    }

    private _updateButtonStates(): void {
        const currentLevel = this.tuneData.indentLevel;

        this.decreaseButton.disabled = currentLevel <= this.minIndentLevel;
        this.decreaseButton.classList.toggle(this._CSS.buttonDisabled, this.decreaseButton.disabled);

        this.increaseButton.disabled = currentLevel >= this.maxIndentLevel;
        this.increaseButton.classList.toggle(this._CSS.buttonDisabled, this.increaseButton.disabled);
    }

    /**
     * This is the TUNE'S save method. It returns the data for THIS TUNE.
     * Editor.js will store this data under block.tunes.indentTune.
     * @returns {TuneData} - The data object for this tune.
     */
    save(): TuneData {
        // console.log(`IndentTune save() for block ${this.block.id} (${this.block.name}): Returning`, this.tuneData);
        return {
            indentLevel: this.tuneData.indentLevel // Return a copy or the direct object
        };
    }

    /**
     * Executed when a Block is rendered or re-rendered.
     * Use this to apply styles based on the tune's current (loaded) state.
     * The `blockContentElement` is the direct output of the Tool (e.g., a P tag).
     * We are applying styles to `.ce-block__content` or `this.block.holder` via `_applyIndentStyles`.
     */
    wrap(blockContentElement: HTMLElement): void {
        // The `data` in the constructor (this.tuneData) should already have the correct indentLevel.
        // Styles are applied in render() and when indent changes.
        // We might re-apply here to be safe if the block re-renders for other reasons.
        // console.log(`IndentTune wrap() for block ${this.block.id} (${this.block.name}). current indentLevel: ${this.tuneData.indentLevel}. Re-applying styles.`);
        this._applyIndentStyles(this.tuneData.indentLevel);
    }

    /**
     * Helper to dispatch a generic 'input' event on the block's holder.
     * This can help trigger Editor.js's onChange or other listeners,
     * ensuring that the editor knows the block's data (including tunes) might have changed.
     */
    private _dispatchBlockChanged(): void {
        const event = new CustomEvent('block-changed', { // Or 'input', or a more specific custom event
            bubbles: true,
            cancelable: true,
            detail: {
                target: this.block, // Pass block API for context if needed
                // You could also pass the tune instance if Editor.js uses it
            }
        });
        this.block.holder.dispatchEvent(event);
        // console.log(`IndentTune for block ${this.block.id}: Dispatched 'block-changed' event.`);
    }

    static get allowedBlocks(): string[] {
        return ['paragraph', 'header', 'list', 'quote'];
    }

    static isReadOnlySupported(): boolean {
        return true;
    }
}