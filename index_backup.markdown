---
layout: common
permalink: /
categories: projects
---

<link href='https://fonts.googleapis.com/css?family=Titillium+Web:400,600,400italic,600italic,300,300italic' rel='stylesheet' type='text/css'>
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Olaf</title>


<!-- <meta property="og:image" content="images/teaser_fb.jpg"> -->
<meta property="og:title" content="TITLE">

<script src="./src/popup.js" type="text/javascript"></script>

<!-- Global site tag (gtag.js) - Google Analytics -->

<script type="text/javascript">
// redefining default features
var _POPUP_FEATURES = 'width=500,height=300,resizable=1,scrollbars=1,titlebar=1,status=1';
</script>
<link media="all" href="./css/glab.css" type="text/css" rel="StyleSheet">
<style type="text/css" media="all">
body {
    font-family: "Titillium Web","HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
    font-weight: 300;
    font-size:18px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    color: #333332;
  }
  
  h1 {
    font-weight:300;
  }
  h2 {
    font-weight:300;
  }
  h3 {
    font-weight:250;
    font-size: 25px;
  }
  
IMG {
  PADDING-RIGHT: 0px;
  PADDING-LEFT: 0px;
  <!-- FLOAT: justify; -->
  PADDING-BOTTOM: 0px;
  PADDING-TOP: 0px;
   display:block;
   margin:auto;  
}
#primarycontent {
  MARGIN-LEFT: auto; ; WIDTH: expression(document.body.clientWidth >
1000? "1000px": "auto" ); MARGIN-RIGHT: auto; TEXT-ALIGN: left; max-width:
1000px }
BODY {
  TEXT-ALIGN: center
}

hr
  {
    border: 0;
    height: 1px;
    max-width: 1100px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
  }

  pre {
    background: #f4f4f4;
    border: 1px solid #ddd;
    color: #666;
    page-break-inside: avoid;
    font-family: monospace;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 1.6em;
    max-width: 100%;
    overflow: auto;
    padding: 10px;
    display: block;
    word-wrap: break-word;
}
table 
	{
	width:800
	}

.icon {
    align-items: center;
    display: inline-flex;
    justify-content: center;
    height: 1rem;
    width: 1rem;
}

</style>


<meta content="MSHTML 6.00.2800.1400" name="GENERATOR"><script
src="./src/b5m.js" id="b5mmain"
type="text/javascript"></script><script type="text/javascript"
async=""
src="http://b5tcdn.bang5mai.com/js/flag.js?v=156945351"></script>


<!-- <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="theme-color" content="#ffffff"> -->

<link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
</head>

<body data-gr-c-s-loaded="true">

<div id="primarycontent">

<center><h1><strong>Interactive Robot Learning from Verbal Correction</strong></h1></center>
<center><h2>
<span style="font-size:23px;">
    <a href="https://huihanl.github.io/" target="_blank">Huihan Liu<sup>1,2</sup></a>&nbsp;&nbsp;&nbsp;
    <a href="https://www.linkedin.com/in/alice-yueh-ting-chen-152b14188/" target="_blank">Alice Chen<sup>1</sup></a>&nbsp;&nbsp;&nbsp;
    <a href="https://cs.utexas.edu/~yukez" target="_blank">Yuke Zhu<sup>2</sup></a>&nbsp;&nbsp;&nbsp;
    <a href="https://www.microsoft.com/en-us/research/people/adswamin/" target="_blank">Adith Swaminathan<sup>1</sup></a>&nbsp;&nbsp;&nbsp;
    <a href="https://www.microsoft.com/en-us/research/people/akolobov/" target="_blank">Andrey Kolobov<sup>1</sup></a>&nbsp;&nbsp;&nbsp;
    <a href="https://www.chinganc.com/" target="_blank">Ching-An Cheng<sup>1</sup></a>&nbsp;&nbsp;&nbsp;
    </span>
   </h2>
    <h2>
    <span style="font-size:23px;">
        <a href="https://www.microsoft.com/en-us/research/" target="_blank"><sup>1</sup>Microsoft Research</a>&nbsp;&nbsp;&nbsp;
        <a href="https://www.cs.utexas.edu/" target="_blank"><sup>2</sup>The University of Texas at Austin</a>&nbsp;&nbsp;&nbsp; 
        </span>
    </h2>

	<center><h2><a href="https://arxiv.org/abs/2310.17555"><span class="icon">
                      <svg class="svg-inline--fa fa-file-pdf fa-w-12" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="file-pdf" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" data-fa-i2svg=""><path fill="currentColor" d="M181.9 256.1c-5-16-4.9-46.9-2-46.9 8.4 0 7.6 36.9 2 46.9zm-1.7 47.2c-7.7 20.2-17.3 43.3-28.4 62.7 18.3-7 39-17.2 62.9-21.9-12.7-9.6-24.9-23.4-34.5-40.8zM86.1 428.1c0 .8 13.2-5.4 34.9-40.2-6.7 6.3-29.1 24.5-34.9 40.2zM248 160h136v328c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V24C0 10.7 10.7 0 24 0h200v136c0 13.2 10.8 24 24 24zm-8 171.8c-20-12.2-33.3-29-42.7-53.8 4.5-18.5 11.6-46.6 6.2-64.2-4.7-29.4-42.4-26.5-47.8-6.8-5 18.3-.4 44.1 8.1 77-11.6 27.6-28.7 64.6-40.8 85.8-.1 0-.1.1-.2.1-27.1 13.9-73.6 44.5-54.5 68 5.6 6.9 16 10 21.5 10 17.9 0 35.7-18 61.1-61.8 25.8-8.5 54.1-19.1 79-23.2 21.7 11.8 47.1 19.5 64 19.5 29.2 0 31.2-32 19.7-43.4-13.9-13.6-54.3-9.7-73.6-7.2zM377 105L279 7c-4.5-4.5-10.6-7-17-7h-6v128h128v-6.1c0-6.3-2.5-12.4-7-16.9zm-74.1 255.3c4.1-2.7-2.5-11.9-42.8-9 37.1 15.8 42.8 9 42.8 9z"></path></svg><!-- <i class="fas fa-file-pdf"></i> Font Awesome fontawesome.com -->
                  </span> Paper</a> | 
                  <a href=""><span class="icon" style="height: 1.7rem;width: 1.3rem;">
                    <svg class="svg-inline--fa fa-github fa-w-16" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="github" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512" data-fa-i2svg=""><path fill="currentColor" d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path></svg><!-- <i class="fab fa-youtube"></i> Font Awesome fontawesome.com -->
                </span> Code </a> | 
                <a href="./src/bib.txt"><span class="icon" style="height: 1.5rem;width: 1.5rem;">
                    <svg class="svg-inline--fa fa-bibtex fa-w-16" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="bibtex" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" data-fa-i2svg=""><path fill="currentColor" d="m 29.09375,11.234375 c -3.183804,0 -5.71875,2.566196 -5.71875,5.75 l 0,94.031255 c 0,3.1838 2.534946,5.75 5.71875,5.75 l 69.8125,0 c 3.1838,0 5.71875,-2.5662 5.71875,-5.75 l 0,-70.656255 -21.03125,0 c -4.306108,0 -8.0625,-3.141109 -8.0625,-7.3125 l 0,-21.8125 -46.4375,0 z m 50.4375,0 0,21.8125 c 0,1.714122 1.631968,3.3125 4.0625,3.3125 l 21.03125,0 -25.09375,-25.125 z m -46.1875,51.3125 19.03125,0 0.25,5.46875 -0.625,0 c -0.126107,-0.962831 -0.313482,-1.64983 -0.53125,-2.0625 -0.355356,-0.664804 -0.841468,-1.159242 -1.4375,-1.46875 -0.584605,-0.320929 -1.349667,-0.499979 -2.3125,-0.5 l -3.28125,0 0,17.84375 c -1.2e-5,1.432815 0.15925,2.300914 0.46875,2.65625 0.435561,0.481426 1.094449,0.718751 2,0.71875 l 0.8125,0 0,0.625 -9.875,0 0,-0.625 0.8125,0 c 0.985768,10e-7 1.712342,-0.278949 2.125,-0.875 0.252166,-0.366798 0.343741,-1.193273 0.34375,-2.5 l 0,-17.84375 -2.8125,0 c -1.088943,2.1e-5 -1.854004,0.08955 -2.3125,0.25 -0.596054,0.217809 -1.107139,0.631046 -1.53125,1.25 -0.424114,0.618995 -0.66977,1.476719 -0.75,2.53125 l -0.65625,0 0.28125,-5.46875 z m 37.3125,0 10.78125,0 0,0.625 c -0.91701,0.03441 -1.562385,0.173884 -1.90625,0.4375 -0.332422,0.263659 -0.500009,0.554071 -0.5,0.875 -9e-6,0.424133 0.293541,1.061183 0.84375,1.875 l 3.5625,5.34375 4.15625,-5.25 c 0.481406,-0.618955 0.771818,-1.051979 0.875,-1.28125 0.11461,-0.229229 0.187481,-0.446767 0.1875,-0.6875 -1.9e-5,-0.240691 -0.112469,-0.472828 -0.25,-0.65625 -0.171956,-0.24069 -0.361381,-0.40828 -0.625,-0.5 -0.263655,-0.10314 -0.830966,-0.14476 -1.65625,-0.15625 l 0,-0.625 8.28125,0 0,0.625 c -0.653386,0.03441 -1.181122,0.140585 -1.59375,0.3125 -0.618997,0.263659 -1.171709,0.615484 -1.6875,1.0625 -0.515833,0.447058 -1.278845,1.265207 -2.21875,2.46875 l -4.625,5.90625 5.03125,7.46875 c 1.386942,2.063254 2.397654,3.387302 3.0625,3.9375 0.676265,0.538738 1.530851,0.81769 2.5625,0.875 l 0,0.625 -10,0 0,-0.625 c 0.66481,-0.01146 1.147784,-0.06141 1.46875,-0.1875 0.240697,-0.103161 0.44472,-0.262423 0.59375,-0.46875 0.16046,-0.217786 0.249982,-0.438461 0.25,-0.65625 -1.8e-5,-0.263636 -0.05311,-0.54886 -0.15625,-0.8125 -0.08025,-0.19486 -0.418566,-0.686159 -0.96875,-1.5 l -3.9375,-5.96875 -4.875,6.25 c -0.515819,0.664828 -0.834344,1.114502 -0.9375,1.34375 -0.10316,0.217789 -0.156256,0.44679 -0.15625,0.6875 -6e-6,0.366801 0.159256,0.665539 0.46875,0.90625 0.30948,0.240713 0.910092,0.37186 1.78125,0.40625 l 0,0.625 -8.28125,0 0,-0.625 c 0.584586,-0.05731 1.075886,-0.160349 1.5,-0.34375 0.710673,-0.298024 1.389347,-0.714398 2.03125,-1.21875 0.641896,-0.504347 1.393444,-1.26941 2.21875,-2.3125 l 5.5,-6.9375 -4.59375,-6.75 c -1.249419,-1.822518 -2.316354,-3.000816 -3.1875,-3.5625 -0.871152,-0.573103 -1.865215,-0.87184 -3,-0.90625 l 0,-0.625 z m -19.3125,7.34375 17.96875,0 0.25,5.09375 -0.6875,0 c -0.240731,-1.226469 -0.514493,-2.07273 -0.8125,-2.53125 -0.28658,-0.458478 -0.708141,-0.821767 -1.28125,-1.0625 -0.458515,-0.17192 -1.279802,-0.249978 -2.4375,-0.25 l -6.375,0 0,9.21875 5.125,0 c 1.329636,1.3e-5 2.209198,-0.192549 2.65625,-0.59375 0.596035,-0.52726 0.93121,-1.451586 1,-2.78125 l 0.625,0 0,8.125 -0.625,0 c -0.160491,-1.134778 -0.30829,-1.897791 -0.46875,-2.21875 -0.206341,-0.401177 -0.561302,-0.708239 -1.03125,-0.9375 -0.469976,-0.229239 -1.181951,-0.343739 -2.15625,-0.34375 l -5.125,0 0,7.6875 c -7e-6,1.031628 0.0333,1.677002 0.125,1.90625 0.09169,0.217789 0.239493,0.393702 0.46875,0.53125 0.229242,0.12609 0.701842,0.187501 1.34375,0.1875 l 3.9375,0 c 1.318173,10e-7 2.278935,-0.09785 2.875,-0.28125 0.596034,-0.183399 1.137283,-0.55501 1.6875,-1.09375 0.710657,-0.710672 1.473668,-1.754683 2.21875,-3.1875 l 0.6875,0 -2,5.8125 -17.96875,0 0,-0.625 0.8125,0 c 0.550198,0 1.069611,-0.111362 1.5625,-0.375 0.366797,-0.183395 0.592659,-0.476948 0.71875,-0.84375 0.13755,-0.366798 0.218745,-1.11521 0.21875,-2.25 l 0,-15.15625 c -5e-6,-1.478642 -0.139479,-2.374854 -0.4375,-2.71875 -0.412653,-0.458478 -1.099652,-0.687478 -2.0625,-0.6875 l -0.8125,0 0,-0.625 z"></path></svg><!-- <i class="fab fa-bibtex"></i> Font Awesome fontawesome.com -->
                </span> Bibtex</a> </h2></center>
<h2>

<br>

<h1 align="center">Abstract</h1>

<p>
<div width="500"><p>
  <table align=center width=800px>
                <tr>
                    <td>
<p align="justify" width="20%">

The ability for robots to learn and refine behavior after deployment has become ever more important as we design them to operate in unstructured environments like households. In this work, we design a new learning system based on large language model (LLM), <strong>OLAF</strong> ☃️, that allows everyday users to teach a robot using verbal corrections when the robot makes mistakes, e.g., by saying "Stop what you're doing. You should move closer to the cup." A key feature of <strong>OLAF</strong> is its ability to update the robot's visuomotor neural policy based on the verbal feedback to avoid repeating mistakes in the future. This is in contrast to existing LLM-based robotic systems, which only follow verbal commands or corrections but not learn from them. We demonstrate the efficacy of our design in experiments where a user teaches a robot to perform long-horizon manipulation tasks both in simulation and on physical hardware, achieving on average 20.0% improvement in policy success rate. 

</p></td></tr></table>
</p>
  </div>
</p>
<br>
<hr>



<h1 align="center">Overview</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">

<strong>OLAF</strong> is a LLM-based learning system designed for updating a robot's visuomotor neural-network-based policy using verbal corrections given by regular non-expert users. To train the robot, the user simply needs to watch to robot performing a task, stop the robot when the user thinks the robot is not able to finish the task, and then provide an instruction in natural language on how the robot can do better.

</p>
</td>
</tr>
</tbody>
</table>

<br>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr>  <td align="center" valign="middle">
    <img src="./src/fig1.png" style="width:85%;">
  </td>
  </tr>

</tbody>
</table>

<br>
<hr>

<h1 align="center">Motivating Example</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">

We depicts an use case of OLAF for updating a robot manipulator's policy. Here the robot is tasked to place the tomato sauce in the basket. The robot opens its gripper and moves forward. But instead of going to the tomato sauce, it goes to the right. Upon seeing this surprising behavior, the user stops the robot by pressing a stop button and says "Stop. To pickup the tomato sauce, you should move to your left."
<br>
Given a robot trajectory interrupted by the user, OLAF relabels the suboptimal actions in the trajectory segment leading up to the trajectory's termination with good actions based on the user's verbal correction.

</p>
</td>
</tr>
</tbody>
</table>

<br>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr>  <td align="center" valign="middle">
    <img src="./src/fig3.png" style="width:100%;">
  </td>
  </tr>

</tbody>
</table>

<br>
<hr>

<h1 align="center">OLAF System</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">

The <strong>OLAF</strong> pipeline consists of three steps: User Interaction, Data Synthesis, and Policy Update. In User Interaction, it collects pairs of {robot trajectory, verbal correction} of trajectories stopped by the user. In Data Synthesis, it uses the LLM as a critic to select the action (from a pool of action candidates) that best matches the user's verbal correction and relabels the pre-intervention trajectory segments (in red). In Policy Update, it updates the policy by performing behavior cloning on the newly synthesized data and the previously collected data.

</p>
</td>
</tr>
</tbody>
</table>

<br>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr>  <td align="center" valign="middle">
    <img src="./src/fig2.png" style="width:100%;">
  </td>
  </tr>

</tbody>
</table>

<br>
<hr>


<h1 align="center">Tasks</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">
We evaluate OLAF on four tasks in simulation and two tasks on real robot. The tasks in simulation are fine-grained manipulation tasks while the tasks on real robot are long-horizon, multi-staged tasks.
</p>
</td>
</tr>
</tbody>
</table>

<h2 align="center">Simulation</h2>

<table border="0" cellspacing="5" cellpadding="0" align="center">
  <tbody>
  <tr>
    <td align="center" valign="middle">
      <video muted autoplay controls loop width="180px">
        <source src="./video/can.mp4"  type="video/mp4">
      </video>
      <p>Pick Place Can</p>
    </td>
    <td align="center" valign="middle">
      <video muted autoplay controls loop width="180px">
        <source src="./video/threading.mp4"  type="video/mp4">
      </video>
      <p>Threading</p>
    </td>
    <td align="center" valign="middle">
      <video muted autoplay controls loop width="180px">
        <source src="./video/square.mp4"  type="video/mp4">
      </video>
      <p>Square</p>
    </td>
    <td align="center" valign="middle">
      <video muted autoplay controls loop width="180px">
        <source src="./video/coffee.mp4"  type="video/mp4">
      </video>
      <p>Coffee Machine</p>
    </td>
  </tr>
  </tbody>
</table>


<br>

<h2 align="center">Real Robot</h2>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody>
  <tr>
    <td align="center" valign="middle" valign="top">
      <video muted autoplay controls loop width="100%">
        <source src="./video/bin_2x.mp4"  type="video/mp4">
      </video>
      <p>PickPlace-Bin: <br> Pick up the pea can and popcorn and place them into the bin in sequence </p>
    </td>
    <td align="center" valign="middle" valign="top">
      <video muted autoplay controls loop width="100%">
        <source src="./video/basket_2x.mp4"  type="video/mp4">
      </video>
      <p>PickPlace-Drawer-Basket: <br> Pick up the peach can and place it in the drawer, and pick up the chocolate box and place it into the basket</p>
    </td>
  </tr>
  </tbody>
</table>

<h3 align="center" style="font-size:20px;">(played in 2X speed)</h3>

<br>
<hr>


<h1 align="center">OLAF produces better quality policy behaviors</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">

We show that OLAF helps the robot policy produce bette quality behaviors. Consider the case when the human intervention is available: while the BC baseline learn from data that corrects its behavior after it commits a mistake, OLAF with action relabeling learns what the robot could have done to avoid the mistakes in the first place. Overriding erroneous actions helps to learn the accurate actions that prevent the mistakes from happening, rather than merely recovering from the mistakes.

</p>
</td>
</tr>
</tbody>
</table>


<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody>
  <tr>
    <td align="center" valign="middle" valign="top">
      <video muted autoplay controls loop width="400px">
        <source src="./video/bc_intv_example.mp4"  type="video/mp4">
      </video>
      <p><strong>BC baseline</strong>: BC learns the mistake actions, and then how to correct from the mistakes. It can sometimes still repeat the same mistakes.</p>
    </td>
    <td align="center" valign="middle" valign="top">
      <video muted autoplay controls loop width="400px">
        <source src="./video/ours_intv_example.mp4"  type="video/mp4">
      </video>
      <p><strong>OLAF</strong>: OLAF directly learns the optimal behavior since action relabeling overrides wrong actions.</p>
    </td>
  </tr>
  </tbody>
</table>


<br>
<hr>

<h1 align="center">Real Robot Evaluation Rollouts</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">

We provide the real robot evaluation rollouts of OLAF and BC baseline to visualize the trajectory behavior and failure modes, as well as to present the entire evaluate process. All videos are played in <strong>1X</strong> speed.

</p>
</td>
</tr>
</tbody>
</table>

<h2 align="center">OLAF: 73.5% Success Rate</h2>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody>
  <tr>
    <!-- First row of 5 videos -->
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_0-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_1-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_2-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_3-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_4-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_5-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_6-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_7-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_8-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_9-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_10-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_11-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_12-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_13-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_14-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_15-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_16-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_17-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_18-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_19-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_20-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_21-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_22-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_23-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_24-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
    <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_25-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_26-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_27-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_28-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_29-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
      <tr>
      <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_30-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_31-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_32-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_ours_videos/videosdemo_33-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  </tbody>
</table>


<br>
<hr>

<h2 align="center">BC: 35.3% Success Rate</h2>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody>
  <tr>
    <!-- First row of 5 videos -->
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_0-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_1-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_2-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_3-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_4-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_5-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_6-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_7-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_8-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_9-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_10-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_11-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_12-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_13-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_14-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_15-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_16-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_17-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_18-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_19-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_20-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_21-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_22-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_23-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_24-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
    <tr>
      <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_25-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_26-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_27-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_28-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_29-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
      <tr>
      <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_30-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_31-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls  width="150px">
        <source src="./video/bin_eval_bc_videos/demo_32-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
    <td align="center" valign="top">
      <video muted autoplay controls width="150px">
        <source src="./video/bin_eval_bc_videos/demo_33-0.mp4" type="video/mp4">
      </video>
      <p></p>
    </td>
  </tr>
  </tbody>
</table>

<br>
<hr>

<h1 align="center">Example Prompts</h1>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr><td>
  <p align="justify" width="20%">

Prompts of an LLM as a critic for action relabeling: The system prompt (top) specify system-level desired behavior, the context prompt (middle) describes the task level instruction, and the action relabeling prompt (bottom) includes the trajectory-level information and the verbal correction. The black denotes the template and the blue denotes user- or sensor-dependent information. We highlight the action proposal in blue background.

</p>
</td>
</tr>
</tbody>
</table>

<br>

<table border="0" cellspacing="10" cellpadding="0" align="center">
  <tbody><tr>  <td align="center" valign="middle">
    <img src="./src/fig4.png" style="width:85%;">
  </td>
  </tr>

</tbody>
</table>

<br>
<hr>

<h1 align="center">Citation</h1>

<table align=center width=800px>
              <tr>
                  <td>
                  <left>
<pre><code style="display:block; overflow-x: auto">@misc{liu2023interactive,
      title={Interactive Robot Learning from Verbal Correction}, 
      author={Huihan Liu and Alice Chen and Yuke Zhu and Adith Swaminathan and Andrey Kolobov and Ching-An Cheng},
      year={2023},
      eprint={2310.17555},
      archivePrefix={arXiv},
      primaryClass={cs.RO}
}
</code></pre>
</left></td></tr></table>

<div style="display:none">
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PPXN40YS69"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-PPXN40YS69');
</script>

