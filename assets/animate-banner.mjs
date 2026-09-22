/**
 * Add a six-second ambient loop to the existing anime illustration.
 * Requires ffmpeg on PATH. No generated faces, camera movement or text animation.
 * Run: node assets/animate-banner.mjs
 */
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const dir=path.dirname(fileURLToPath(import.meta.url));
const tau='6.28318530718';
// The rain is confined to the window behind the desk and character.
// After 72 frames, 4*72 is an exact multiple of the 96-pixel rain period.
const windowMask='gt(X,410)*lt(X,840)*lt(Y,143)+gte(X,840)*lt(X,1020)*lt(Y,58)';
const rain=`min(1,${windowMask})*lt(mod(X+Y*0.075,23),1.15)*lt(mod(Y-N*4+floor(X/23)*19,96),12)*45`;
// Low amplitude, slow CRT illumination. No flashes or strobing.
const crtMask='between(X,563,710)*between(Y,151,265)+between(X,754,862)*between(Y,170,274)';
const crt=`min(1,${crtMask})*(2+2*sin(N*${tau}/72))`;
const filter=[
 '[0:v]scale=1200:400:flags=lanczos,format=rgba[base]',
 `[1:v]format=rgba,geq=r=155:g=217:b=222:a='${rain}+${crt}'[ambience]`,
 '[base][ambience]overlay=shortest=1:format=auto,split[frames][colors]',
 '[colors]palettegen=max_colors=256:stats_mode=diff[palette]',
 '[frames][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[out]'
].join(';');
const run=spawnSync('ffmpeg',['-hide_banner','-loglevel','warning','-y','-loop','1','-framerate','12','-i',path.join(dir,'night-shift.png'),'-f','lavfi','-i','color=c=black@0.0:s=1200x400:r=12:d=6','-filter_complex',filter,'-map','[out]','-t','6','-loop','0','-gifflags','+transdiff',path.join(dir,'night-shift.gif')],{stdio:'inherit'});
if(run.error)throw run.error;
process.exitCode=run.status??1;
