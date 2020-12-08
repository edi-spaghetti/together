
class Shader {

    constructor(gl) {
        this.gl = gl;

        const vertSource = `
            attribute vec2 vertex;
            void main() {
                gl_Position = vec4(vertex, 0.0, 1.0);
            }
        `;

        const fragSource = `
            void main() {
                gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
        `;

        this.ID = this.initShaderProgram(vertSource, fragSource);
        this.info = {
            attrib: {
                vertex: this.gl.getAttribLocation(this.ID, 'vertex'),
            },
//            uniform: {
//                projection: gl.getUniformLocation(this.ID, 'projection'),
//                modeView: gl.getUniformLocation(this.ID, 'modelView')
//            }
        };
        this.buffers = this.initBuffers();
    }

    update() {

    }

    draw() {
        this.gl.useProgram(this.ID);
        this.gl.drawArrays(this.gl.TRIANGLES, 0, 3);
        console.log('drew!');
    }

    initShaderProgram(vert, frag) {
        const vert_id = this.loadShader(this.gl.VERTEX_SHADER, vert);
        const frag_id = this.loadShader(this.gl.FRAGMENT_SHADER, frag);
        const id = this.gl.createProgram();
        this.gl.attachShader(id, vert_id);
        this.gl.attachShader(id, frag_id);
        this.gl.linkProgram(id);

        if (!this.gl.getProgramParameter(id, this.gl.LINK_STATUS)) {
            alert('Cannot init shader program');
            return null;
        }
        return id;
    }

    loadShader(type, source) {
        console.log(type);
        const shader = this.gl.createShader(type);
        this.gl.shaderSource(shader, source);
        this.gl.compileShader(shader);

        if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) {
            alert('Cannot load shader');
            this.gl.deleteShader(shader);
            return null;
        }
        else {
            console.log('Loaded shader');
        }
        return shader;
    }

    initBuffers() {
        const VBO = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, VBO);
        const positions = [0.0, 0.5,  -0.5, -0.5,  0.5, -0.5];
        this.gl.bufferData(
            this.gl.ARRAY_BUFFER,
            new Float32Array(positions),
            this.gl.STATIC_DRAW
        );

        this.gl.vertexAttribPointer(
            this.info.attrib.vertex,
            2,
            this.gl.FLOAT,
            false,
            0,
            0
        );
        this.gl.enableVertexAttribArray(this.info.attrib.vertex)

        return VBO

    }
}