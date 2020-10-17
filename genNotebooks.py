from bs4 import BeautifulSoup, SoupStrainer, NavigableString
from urllib.parse import urljoin
import textwrap
import requests
import re
import json

import requests_cache
requests_cache.install_cache( "dev_cache", allowable_methods=("GET", "POST") );


baseurl = "https://codingbat.com/java";

response = requests.get( baseurl );

"""
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Warmup-1 > sleepIn\n",
    "\n",
    "```\n",
    "The parameter weekday is true if it is a weekday, and the parameter vacation is true if we are on vacation. We sleep in if it is not a weekday or we're on vacation. Return true if we sleep in.\n",
    "\n",
    "\n",
    "sleepIn(false, false) → true\n",
    "sleepIn(true, false) → false\n",
    "sleepIn(false, true) → true\n",
    "```"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "bool sleepIn(bool weekday, bool vacation)\n",
    "{\n",
    "    return true;\n",
    "}\n",
    "\n",
    "// tests:\n",
    "printTest( \"sleepIn(false, false) → true\", sleepIn(false, false), true );\n",
    "printTest( \"sleepIn(true, false) → false\", sleepIn(true, false), false );\n",
    "printTest( \"sleepIn(false, true) → true\", sleepIn(false, true), true );\n",
    "printTest( \"sleepIn(true, true) → true\", sleepIn(true, true), true );"
   ]
  }
"""

nbStub = \
"""
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#include <iostream>\\n",
    "#include <iomanip>\\n",
    "#include <vector>\\n",
    "\\n",
    "using namespace std;"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "template<class A>\\n",
    "void printTest( string str, A run, A expected )\\n",
    "{\\n",
    "    if( run == expected )\\n",
    "        cout << boolalpha << \\"\\\\033[1;32m\\"\\n",
    "            << \\"Expected: \\" << setw(60) << left << str << \\" Run: \\" << setw(20) << left << run << \\"\\\\t\\\\tOK\\"\\n",
    "            << \\"\\\\033[0m\\" << endl;\\n",
    "    else\\n",
    "        cerr << boolalpha << \\"\\\\033[1;31m\\"\\n",
    "            << \\"Expected: \\" << setw(60) << left << str << \\" Run: \\" << setw(20) << left << run << \\"\\\\t\\\\tX\\"\\n",
    "            << \\"\\\\033[0m\\" << endl;\\n",
    "}\\n",
    "void printTest( string str, string run, const char* expected ){ printTest( str, \\"\\\\\\"\\"+run+\\"\\\\\\"\\", \\"\\\\\\"\\"+string( expected )+\\"\\\\\\"\\" ); }\\n",
    "template<class A>\\n",
    "void printTest( string str, vector<A> run, vector<A> expected )\\n",
    "{\\n",
    "  string runStr = \\"[\\"; for( A a : run ) runStr += to_string( a ) + \\", \\";\\n",
    "  if( runStr.length() > 1 ) runStr = runStr.substr(0, runStr.length()-2); runStr += \\"]\\";\\n",
    "  string expStr = \\"[\\"; for( A a : expected ) expStr += to_string( a ) + \\", \\";\\n",
    "  if( expStr.length() > 1 ) expStr = expStr.substr(0, expStr.length()-2); expStr += \\"]\\";\\n",
    "  printTest( str, runStr, expStr );\\n",
    "}"
   ]
  },
CODINGBAT_PROBLEMS_HERE
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "C++17",
   "language": "C++17",
   "name": "xcpp17"
  },
  "language_info": {
   "codemirror_mode": "text/x-c++src",
   "file_extension": ".cpp",
   "mimetype": "text/x-c++src",
   "name": "c++",
   "version": "17"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
""";

i = 0;
for link in BeautifulSoup(response.text, parse_only=SoupStrainer('a'), features="html.parser"):
	if link.has_attr('href') and str.startswith( link[ "href" ], "/java/" ):
		print(link['href'])

		out = "";

		resp = requests.get( urljoin( baseurl, link[ "href" ] ) );
		for problem in BeautifulSoup( resp.text, parse_only=SoupStrainer( "a" ), features="html.parser" ):
			if problem.has_attr( "href" ) and str.startswith( problem[ "href" ], "/prob/" ):
				print( "\t", problem["href"] );

				r = requests.get( urljoin( baseurl, problem[ "href" ] ) );
				bs = BeautifulSoup( r.text, features="html.parser" );

				problemInfo = [];
				el = bs.select_one( ".go" ).parent.previousSibling;
				while el != None:
					if not isinstance(el, NavigableString) and el.has_attr( "class" ) and "minh" in el[ "class" ]: problemInfo.insert( 0, "" );
					problemInfo.insert( 0, textwrap.fill( el.string or "", 80 ) );
					el = el.previousSibling;

				problemStatement = "\n".join( problemInfo ).replace( "\n\n", "\n" );

				templateCode = bs.select_one( "#ace_div" ).string;

				dummyRets = {
					"int": "0",
					"boolean": "false",
					"String": "\"\"",
					"int[]": "new int[]{}"
				}
				retType = ( re.search( r"public (.*?) ", templateCode ) or re.search( r"^(.*?) ", templateCode )).group( 1 );

				dummySubmittableJava = templateCode.replace( "  \n}", "    return " + dummyRets[retType] + ";\n}" );
				testsResp = requests.post( "https://codingbat.com/run", data={ "id": problem["href"][len("/prob/"):], "code": dummySubmittableJava } );
				tests = [ test.select_one( "td" ).string for test in BeautifulSoup( testsResp.text, parse_only=SoupStrainer( "tr" ), features="html.parser" ) if test.select_one( "td" ) ];
				

				celljson = {
				   "cell_type": "markdown",
				   "metadata": {}
				  }
				problemTitle = bs.select_one( "span.h2" ).string \
							 + bs.select_one( "span.h2" ).parent.nextSibling.string \
							 + bs.select_one( "span.h2" ).parent.nextSibling.nextSibling.string;
				problemMDSource = f"# {problemTitle}";

				celljson[ "source" ] = [ line + "\n" for line in problemMDSource.split( "\n" ) ];
				celljson[ "source" ][-1] = celljson[ "source" ][-1][:-1];
				out += json.dumps( celljson ) + ",\n";

				celljson = {
				   "cell_type": "code",
				   "execution_count": None,
				   "metadata": {},
				   "outputs": [],
				};
				cppSource = f"/*\n{problemStatement}\n*/\n\n"

				dummyCpp = dummySubmittableJava \
					.replace( "public ", "" ) \
					.replace( "boolean", "bool" );
				dummyCpp = re.sub( r"(?<!\w)String", "string", dummyCpp );
				dummyCpp = dummyCpp.replace( "return new int[]{};", "return vector<int>{};" );
				dummyCpp = re.sub( r"(\w+)\[\]", "vector<\\1>", dummyCpp );
				cppSource += dummyCpp;
				cppSource += "\n\n// tests:\n";
				for test in tests:
					if not " → " in test: continue;

					testCall = test.split( " → " )[0].replace("[", "{").replace("]", "}");
					testRet = test.split( " → " )[1].replace("[", "{").replace("]", "}");

					test = test.replace( "\"", "\\\"" );

					cppSource += f"printTest( \"{test}\", {testCall}, {testRet} );\n";

				celljson[ "source" ] = [ line + "\n" for line in cppSource.split( "\n" )[:-1] ];
				celljson[ "source" ][-1] = celljson[ "source" ][-1][:-1];
				out += json.dumps( celljson ) + ",\n";
			


		f = open( f"cpp-codingbat-{str(i+1).zfill(2)}-{link['href'][len('/java/'):]}.ipynb", "w" );
		f.write( nbStub.replace( "CODINGBAT_PROBLEMS_HERE", out[:-2] ) );
		i += 1;
