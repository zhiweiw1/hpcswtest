/*

Copyright 2017 Battelle Energy Alliance, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Description
-----------
HPC Software testing suite.
AbaqusTest subclass source code.

Date Created: Fri Dec 18 15:25:38 MST 2015

Author: Cormac Garvey

*/

#include "generictest.h"

#include <iostream>     // for debugging only
#include <cstdlib>  // for exit()


namespace hpcswtest {


const std::vector<std::string> GenericTest::abaqus_inputs_ = {
R"(*HEADING
*END STEP)"
}; // vector abaqus_inputs_ 
/* In this call, it is just a place holer as GenericTest does not use the input file generated. It uses the one provided in the json file */

/**
* unlike the other apptest  classes with hardcoded module name, Generictest constructor takes the module name from the job script from the Generator class.
*/

GenericTest::GenericTest(const jobscript::JOBSCRIPT &p_s, const std::string &s_a_n): AppTest(module_name(p_s.getModules()[p_s.getModules().size()-1]), ".inp", p_s, abaqus_inputs_.size(), s_a_n),
                                                                                   log_file_name_(getHostName() + "_" + getTestName() + "_test.log"),
                                                                                   result_file_name_(getHostName() + "_" + getTestName() + "_results.out"),
                                                                                   flog_(log_file_name_,std::ios_base::app),
                                                                                   fresult_(result_file_name_,std::ios_base::app) {}


GenericTest::GenericTest(const jobscript::JOBSCRIPT &p_s):AppTest(module_name(p_s.getModules()[p_s.getModules().size()-1]), ".inp", p_s, abaqus_inputs_.size()),
                                                         log_file_name_(getHostName() + "_" + getTestName() + "_test.log"),
                                                         result_file_name_(getHostName() + "_" + getTestName() + "_results.out"),
                                                         flog_(log_file_name_,std::ios_base::app),
                                                         fresult_(result_file_name_,std::ios_base::app) {
std::cout << "Execute runTest: " + module_name(getJobScripts()[0].getModules()[getJobScripts()[0].getModules().size()-1]) << std::endl;
//AppTest(module_name(getJobScripts()[0].getModules()[getJobScripts()[0].getModules().size()-1]), ".inp", p_s, abaqus_inputs_.size());
//AppTest("Generic", ".inp", p_s, abaqus_inputs_.size());
}


void GenericTest::runTest() {
  std::string cmd_result;
  std::string script_cmd_result;
//  std::cout << "Execute runTest member function from AbaqusTest object " << __FILE__ << "\t" <<__LINE__ << std::endl;
  if (!flog_.is_open()) {
      std::cerr << "Error: (" << __FILE__ << "," << __LINE__ << ") Opening file " << log_file_name_ << std::endl;
      exit(EXIT_FAILURE);
  }
  if (!fresult_.is_open()) {
      std::cerr << "Error: (" << __FILE__ << "," << __LINE__ << ") Opening file " << result_file_name_ << std::endl;
      exit(EXIT_FAILURE);
  }
  std::cout << "Testing: " << module_name_version(getJobScripts()[0].getModules()[getJobScripts()[0].getModules().size()-1]) << std::endl;
  int c_i = 0;
//  for (auto abaqus_input: abaqus_inputs_) {//only test one input as described in the argument option for generictest
//    createFileFromStr(getInputFileNames()[c_i], abaqus_input);  
/*no need to creat an input file, it is in the json, and file is in the test-cases directory */
    script_cmd_result = exeAppTest(flog_, fresult_, c_i);
// defined in AppTest class. 
    checkSubmitResult(script_cmd_result, flog_, fresult_);
//defined in helper.cc to check if sbatch return any errro
    ++c_i;
//  }
}


} // namespace hpcswtest

