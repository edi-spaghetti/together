main();

function main() {
    const canvas = document.querySelector('#glCanvas');
    const gl = canvas.getContext('webgl');

    if (!gl) {
        alert('Unable to initialise WebGL. Bad luck.');
        return;
    }

//    shader = new Shader(gl);
//    gl.clearColor(0.0, 0.0, 0.0, 1.0);
//    gl.clear(gl.COLOR_BUFFER_BIT);
//    shader.draw();
}