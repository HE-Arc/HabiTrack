<script setup>
import { ref, onMounted } from "vue";
import moment from "moment";
//Credits: https://codepen.io/Kaperstone/pen/wrZqOV
const props = defineProps({
  propTemplate: {
    type: Object,
  },
  propEntries: {
    type: Array,
    required: true,
  },
});

onMounted(() => {
  /*** draw months ***/

  var month = moment();
  var outputMonth = "<ol class = 'month'>";
  let i = 0;
  for (i = 0; i <= 12; i++) {
    var durationMonth = moment.duration({ months: 1 });
    outputMonth += "<li>";
    outputMonth += moment(month).format("MMM");
    outputMonth += "</li>";
    month = moment(month).subtract(durationMonth);
  }
  outputMonth += "</ol>";

  var output = "<ol><div class = 'week'>";
  var day = moment();

  /* Calculate the offset for days of the week to line up correctly */
  var dayOfWeekOffset = 6 - parseInt(moment().format("d"), 10);
  for (i = 0; i < dayOfWeekOffset; i++) {
    output += "<li class = 'offset'></li>";
  }

  /*** draw calendar ***/
  for (i = 365; i >= 0; i--) {
    let daysEntry = props.propEntries.filter((entry) => {
      return moment(entry.created_at).format("DD-MM-YY") ==
        moment(day).format("DD-MM-YY")
        ? entry
        : null;
    });
    let entry = daysEntry[0];
    output +=
      "<li class=activity-" + (entry ? entry.selected_option : "none") + ">";
    output +=
      '<span class = "tooltip">' + moment(day).format("DD-MM-YY") + "</span>";
    output += "</li>";

    var duration = moment.duration({ days: 1 });
    day = moment(day).subtract(duration);
  }

  output += "</div></ol>";
  document.getElementById("month").innerHTML = outputMonth;
  document.getElementById("days").innerHTML = output;
});
</script>
<template>
  <div class="activity-chart">
    <ol class="days-of-week">
      <li>M</li>
      <li>W</li>
      <li>F</li>
    </ol>
    <div id="month" class="month"></div>
    <div id="days" class="days"></div>
    <div class="key">
      <span>Opt 1</span>
      <ul>
        <li class="activity-3"></li>
        <li class="activity-2"></li>
        <li class="activity-1"></li>
        <li class="activity-0"></li>
        <!--<li class="day-key"></li>-->
      </ul>
      <span>Opt 4</span>
    </div>
  </div>
</template>
<style>
ol,
li {
  padding: 0;
  margin: 0;
  list-style: none;
}
h1 {
  font-size: 1.5em;
  margin: 70px 42px;
}

.activity-chart,
h1 {
  color: #525252;
}
.days li,
.activity-none {
  background: #eee;
}
.activity-chart {
  width: 720px;
  height: 205px;
  padding-left: 110px; /* center in container */
  margin: 50px 150px;
  position: relative;

  /*outline: solid;*/
}

/*** day of week heading ***/

.days-of-week {
  width: 15px;
  position: absolute;
  left: -10px;
  top: 80px;
}

@-moz-document url-prefix() {
  .days-of-week {
    left: 23px;
  }
}

.days-of-week {
  font-size: 0.7em;
}
.days-of-week li:nth-child(2) {
  margin: 13px 0;
}

/*** month headings ***/

.month ol {
  position: absolute;
  top: 40px;
  left: -30px;
}

.month li {
  float: right;
  margin-left: 39px;
  font-size: 0.75em;
}

/*** draw days ***/

.days {
  font-size: 0.75em;
  margin-top: 15px;
  float: right; /* needed to float onto screen */
}

/* offset so days of the week line up
over-specified to win specificity battle */
.activity-chart .offset:hover {
  outline: none;
}
.activity-chart .offset {
  background: none;
}

/* create vertical weeks */
.week {
  width: 108px;
  transform: rotate(90deg);
}

.days li,
.key li {
  width: 12px;
  height: 12px;
  float: right; /* order days starting at the bottom right */
}

.days .bold {
  font-weight: bold;
}
.days li {
  margin: 1.5px;
}

/*** color-code by activity level ***/
.activity-chart .activity-0 {
  background: #681e63;
}
.activity-chart .activity-1 {
  background: #e4a1df;
}
.activity-chart .activity-2 {
  background: #a1e4a6;
}
.activity-chart .activity-3 {
  background: #1e6823;
}

.key {
  position: absolute;
  bottom: 0;
  right: 55px;
}

.key ul {
  display: inline-block;
  margin: 0;
  padding: 0;
}

.key li {
  margin: 0px 2px;
}

/*** tooltips ***/

.days li .tooltip {
  display: none;
}
.days li:hover {
  /*outline disabled due to firefox cross-broswer issue */
  /*outline: 1px solid #555;*/
  position: relative;
  z-index: 3;
}

.days li:hover .tooltip {
  transform: rotate(-90deg);
  display: block;
  position: absolute;
  /* top & left are reversed because the calendar is rotated 90 deg */
  top: -13px;
  left: -85px;
  width: 100px;
  padding: 10px 5px;
  text-align: center;
  background-color: #333;
  color: #f1f1f1;
}

/*** little triangle on the tooltip ***/
.tooltip:before {
  content: "";
  position: absolute;
  width: 0;
  height: 0;

  bottom: -10px;
  right: 50px;

  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 11px solid #333;
}
</style>
