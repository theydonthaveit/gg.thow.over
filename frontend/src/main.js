import { html } from 'lit-html';

const iWasClicked = {
    handleEvent(e) {
        console.log("hi")
    }
}

const myTemplate = (name) => html`<button @click=${iWasClicked}>click me</button>`;

export default myTemplate