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
HPC Software test suite.
RTest is a subclass of pure virtual abstract base class AppTest.

Date Created: Thu Dec 9 15:40:14 MST 2021

Author: Zhiwei Wang

*/

#ifndef HPCSWTEST_PYTHON2TEST_H_
#define HPCSWTEST_PYTHON2TEST_H_

#include "apptest.h"
#include "helper.h"

#include <fstream>


namespace hpcswtest {


class GenericTest: public AppTest {

  public:
    GenericTest(const jobscript::JOBSCRIPT &, const std::vector<std::string> &, const std::string &);
    virtual ~RTest(void) {};
    virtual void runTest(void) override;
    std::vector<std::string> getRModules(void);

  protected:
    void runRModulesTest(std::ofstream &, std::ofstream &, const modules::modules_type &, const std::vector<std::string> &) const;
    void runRTest(std::ofstream &, std::ofstream &, const modules::modules_type &, const std::string &) const;

  private:
    std::string log_file_name_;
    std::string result_file_name_;
    std::ofstream flog_;
    std::ofstream fresult_;
    std::vector<std::string> modules_;
    const static std::vector<std::string> inputs_;

}; // class RTest


} // namespace hpcswtest

#endif  // HPCSWTEST_PYTHON2TEST_H
