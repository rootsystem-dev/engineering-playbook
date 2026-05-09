
## Fran Sans
@font-face {
  font-family: "Fran Sans";
  font-weight: 400;
  font-style: normal;
  src: url("https://freight.cargo.site/m/C2633502019290765743882305316985/FranSans-Solid.woff") format("woff");
}

html {
	--mobile-scale: 1.4;
	--mobile-padding-offset: 1;
}

body {
	--swatch-1: rgba(0, 0, 0, 0.85);
	--swatch-2: rgba(0, 0, 0, 0.75);
	--swatch-3: rgba(0, 0, 0, 0.6);
	--swatch-4: rgba(0, 0, 0, 0.4);
	--swatch-5: rgba(0, 0, 0, 0.25);
	--swatch-6: #000000;
	--colorfilter-color-opacity: 0.72;
	--colorfilter-mix: color-dodge;
	--colorfilter-grayscale: 0.63;
	background-color: #ffffff;
}

body.mobile {
}

a:active,
.linked:active,
.zoomable::part(media):active {
	opacity: 0.7;
}

.page a.active {
	color: #000000;
}

sub {
	position: relative;
	vertical-align: baseline;
	top: 0.3em;
}

sup {
	position: relative;
	vertical-align: baseline;
	top: -0.4em;
}

.small-caps {
	font-variant: small-caps;
	text-transform: lowercase;
}

ol {
	margin: 0;
	padding: 0 0 0 2.5em;
	list-style-type: decimal-leading-zero;
}

ul {
	margin: 0;
	padding: 0 0 0 2.0em;
}

ul.lineated {
	margin: 0;
	padding: 0;
	list-style-type: none;
	margin: 0 0 0 0em;
	text-indent: 0em;
}

blockquote {
	margin: 0;
	padding: 0 0 0 2em;
}

hr {
	background: #000000;
	border: 0;
	height: 1px;
	display: block;
	margin-top: 0.3rem;
	margin-bottom: 0.0rem;
}

.content {
	border-color: rgba(0,0,0,.85);
	border-width: 0.0rem;
	border-style: solid;
	border-radius: 0.0rem;
}

bodycopy {
	font-size: 1.15rem;
	font-weight: 700;
	color: #000000;
	font-family: "Monument Grotesk Variable";
	font-style: normal;
	line-height: 1.05;
	letter-spacing: -0.012em;
	display: block;
	font-variation-settings: 'slnt' 0, 'MONO' 0;
}

.mobile bodycopy {
	font-size: 1rem;
}

bodycopy a {
	color: #000000;
	border-bottom: 0px solid rgba(127, 127, 127, 0.2);
	text-decoration: none;
}

bodycopy a:hover {
}

h1 {
	font-family: "Diatype Variable";
	font-style: normal;
	font-weight: 400;
	margin: 0;
	font-size: 4.5rem;
	line-height: 1;
	color: rgba(0, 0, 0, 0.85);
	letter-spacing: -0.02em;
	font-variation-settings: 'slnt' 0, 'MONO' 0;
}

h1 a {
	color: rgba(0, 0, 0, 0.85);
	text-decoration: none;
}

h1 a:hover {
}

h2 {
	font-family: "Diatype Variable";
	font-style: normal;
	font-weight: 440;
	margin: 0;
	color: rgba(0, 0, 0, 0.85);
	font-size: 3.8rem;
	line-height: 1.1;
	letter-spacing: 0em;
	font-variation-settings: 'slnt' 0, 'MONO' 0;
}

h2 a {
	color: rgba(0, 0, 0, 0.85);
	text-decoration: none;
}

h2 a:hover {
}

.caption {
	font-size: 1.1rem;
	font-weight: 700;
	color: rgba(0, 0, 0, 0.85);
	font-family: "Monument Grotesk Variable";
	font-style: normal;
	line-height: 1.15;
	letter-spacing: 0;
	display: block;
	font-variation-settings: 'slnt' 0, 'MONO' 0;
}

.caption a {
	text-decoration: underline;
	color: rgba(0, 0, 0, 0.85);
}

.caption a:hover {
}

media-item .caption {
	margin-top: .5em;
}

gallery-grid .caption,
gallery-columnized .caption,
gallery-justify .caption {
	margin-bottom: 2em;
}

[thumbnail-index] .caption {
	text-align: center;
}

[thumbnail-index] .caption .tags {
	margin-top: 0.25em;
}

.page {
	justify-content: flex-start;
}

.page-content {
	padding: 0.8rem;
	text-align: left;
}

.mobile [id] .page-layout {
	max-width: 100%;
}

.mobile [id] .page-content {
}

.page-layout {
	align-items: flex-start;
	max-width: 100%;
	padding: 0.0rem;
}

media-item::part(media) {
	border: 0;
	padding: 0;
}

.quick-view {
	height: 100%;
	width: 100%;
	padding: 3rem;
	margin-top: auto;
	margin-right: auto;
	margin-bottom: auto;
	margin-left: auto;
}

.quick-view-background {
	background-color: #ffffff;
}

.quick-view .caption {
	color: rgba(255, 255, 255, 1.0);
	padding: 20px 0;
	text-align: center;
	transition: 100ms opacity ease-in-out;
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
}

.quick-view .caption-background {
	padding: 0.5rem 1rem;
	display: inline-block;
	background: rgba(0, 0, 0, 0.5);
	border-radius: .5rem;
	text-align: left;
	max-width: 50rem;
}

.mobile .quick-view {
	width: 100%;
	height: 100%;
	margin: 0;
	padding: 10px;
}

.mobile .quick-view .caption {
	padding: 10px 0;
}

.body-2 {
	--text-style: "Body 2";
	font-size: 1.45rem;
	font-weight: 400;
	color: rgba(0, 0, 0, 0.85);
	font-family: "Routed Gothic";
	font-style: normal;
	line-height: 1.05;
	letter-spacing: -0.025em;
	display: block;
}

.body-2 a {
	color: rgba(0, 0, 0, 0.85);
	border-bottom: 0px solid rgba(127, 127, 127, 0.2);
	text-decoration: none;
}

.body-2 a:hover {
	
}

.editorial {
	--text-style: "Editorial";
	font-size: 2.25rem;
	font-weight: 400;
	color: rgba(0, 0, 0, 0.85);
	font-family: 'Times', 'Times New Roman', serif;
	font-style: normal;
	line-height: 1.15;
	letter-spacing: -0.008em;
	display: block;
}

.mobile .editorial {
	font-size: 1.6rem;
}

.editorial a {
	color: rgba(0, 0, 0, 0.85);
	border-bottom: 0px solid rgba(127, 127, 127, 0.2);
	text-decoration: none;
}

.editorial a:hover {
	
}

.editorial-mobile {
	--text-style: "Editorial Mobile";
	font-size: 4.30rem;
	font-weight: 400;
	color: #000000;
	font-family: 'Times', 'Times New Roman', serif;
	font-style: normal;
	line-height: 1.05;
	letter-spacing: 0;
	display: block;
}

.mobile .editorial-mobile {
	font-size: 1rem;
}

.editorial-mobile a {
	color: #000000;
	border-bottom: 0px solid rgba(127, 127, 127, 0.2);
	text-decoration: none;
}

.editorial-mobile a:hover {
	
}

.fran-sans {
	--text-style: "FRAN SANS";
	font-size: 5rem;
	font-weight: 400;
	color: #d02a00;
	font-family: Fran Sans;
	font-style: normal;
	line-height: 1;
	letter-spacing: -0.030em;
	display: block;
}

.mobile .fran-sans {
	font-size: 2rem;
}

.fran-sans a {
	color: #d02a00;
	border-bottom: 0px solid rgba(127, 127, 127, 0.2);
	text-decoration: none;
}

.fran-sans a:hover {
	
}

.mobile .quick-view .caption-background {
	max-width: 100vw;
}

::part(slideshow-nav) {
	--button-size: 30px;
	--button-inset: 20px;
	--button-icon-color: rgba(255, 255, 255, 0.9);
	--button-icon-stroke-width: 1.5px;
	--button-icon-stroke-linecap: none;
	--button-background-color: rgba(87, 87, 87, 0.35);
	--button-background-radius: 50%;
	--button-active-opacity: 0.7;
}

gallery-slideshow::part(slideshow-nav) {
	--button-inset: 15px;
}

.quick-view::part(slideshow-nav) {
}

.wallpaper-slideshow::part(slideshow-nav) {
}

.mobile ::part(slideshow-nav) {
	--button-inset: 10px;
}

.mobile .quick-view::part(slideshow-nav) {
	--button-inset: 25px;
}

shop-product {
	font-size: 1.2rem;
	max-width: 22rem;
	font-family: "Diatype Variable";
	font-style: normal;
	font-weight: 400;
	font-variation-settings: 'slnt' 0, 'MONO' 0;
	letter-spacing: 0em;
	margin-bottom: 1em;
}

shop-product::part(price) {
	color: rgba(0, 0, 0, 0.75);
	line-height: 1.1;
	margin-bottom: 0.5em;
}

shop-product::part(dropdown) {
	width: 100%;
	color: rgba(0, 0, 0, 0.85);
	border: 1px solid rgba(0, 0, 0, 0.2);
	background-color: rgba(255, 255, 255, 0.0);
	background-image: url(https://static.cargo.site/assets/images/select-line-arrows.svg);
	background-repeat: no-repeat;
	background-position: top 0em right .1em;
	line-height: 1.2;
	padding: 0.58em 2em 0.55em 0.9em;
	border-radius: 10em;
	margin-bottom: 0.5em;
}

shop-product::part(button) {
	background: rgba(0, 0, 0, 0.15);
	color: rgba(0, 0, 0, 0.75);
	text-align: left;
	line-height: normal;
	padding: 0.5em 1em;
	cursor: pointer;
	border-radius: 10em;
}

shop-product::part(button):active {
	opacity: .7;
}

audio-player {
	--text-color: rgba(0, 0, 0, 0.85);
	--text-padding: 0 1.2em 0 1.0em;
	--background-color: rgba(255, 255, 255, 0);
	--buffer-background-color: rgba(0, 0, 0, 0.03);
	--progress-background-color: rgba(0, 0, 0, 0.075);
	--border-lines: 1px solid rgba(0, 0, 0, 0.2);
	font-size: 1.2rem;
	width: 32rem;
	height: 2.75em;
	font-family: "Diatype Variable";
	font-style: normal;
	font-weight: 400;
	font-variation-settings: 'slnt' 0, 'MONO' 0;
	line-height: normal;
	letter-spacing: 0em;
	margin-bottom: 0.5em;
	border-radius: 10em;
}

audio-player::part(button) {
	--icon-color: rgba(0, 0, 0, 0.85);
	--icon-size: 32%;
	--play-text: '';
	--pause-text: '';
	width: 3.15em;
	display: inline-flex;
	justify-content: center;
	cursor: pointer;
}

audio-player::part(play-icon) {
	padding-left: 0.6em;
}

audio-player::part(pause-icon) {
	padding-left: 0.4em;
}

audio-player::part(progress-indicator) {
	border-right: 1px solid rgba(0, 0, 0, 0);
	height: 100%;
	cursor: ew-resize;
}

audio-player::part(separator) {
	border-right: var(--border-lines);
}

body.mobile audio-player {
	max-width: 100%;
}

[data-predefined-style="true"] bodycopy a:hover {
    color: #179800;
}

.mobile .content {
}

/* Fallback highlight if JavaScript doesn’t run */
::selection,
::-moz-selection {
  background-color: #137102; /* green */
  color: #00decb; /* blue */
}