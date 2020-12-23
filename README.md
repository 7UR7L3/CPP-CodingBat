# CPP-CodingBat
All https://codingbat.com/java problems converted to cpp, in notebook form.

<p align="center">
  <a href="https://mybinder.org/v2/gh/7UR7L3/CPP-CodingBat/master"><img src="https://mybinder.org/badge_logo.svg"></a>
  <br>
  https://mybinder.org/v2/gh/7UR7L3/CPP-CodingBat/master
</p>

(if using CoCalc, note that its c++ runner is a bit buggy; you always have to `restart and run all` as you can't run a cell multiple times, ~~you must replace `vector<foo>` return types with `auto`, and sometimes you must remove comments before the declaration of a function in a cell~~ theoretically i fixed those last two. issues were with needing qualified `std::vector<foo>` in the return types and with an odd number of `'` characters in the cells breaking everything. also the namespace hack for `printTest` is godawful, something is seriously messed up with how cling does or does not overload vs override declarations)
