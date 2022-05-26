#!/usr/bin/env python
#
#Copyright 2017 Battelle Energy Alliance, LLC
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#

"""Read HPC Software test suite output results files, determine
   if results are correct or not and print QA report.

   Initial Version Created on Dec 24, 2015 (by C.Garvey). """


import sys
import os
import re
import socket
import shutil
import glob


NUM_MPI_PROCS = 2
compile_sw_l = ["compiler", "mpi", "blas", "boost"]
dir_sw_l = ["vasp", "lammps", "helios", "cth", "mc21", "nwchem"]

check_file_patterns = {"compiler": {
                                   "file_patterns": {
                                                     "pbs_stdout": ["code is working"]
                                                    },
                                   "files_exist": [],
                                   "check_file_sizes": ["pbs_stderr"]
                                  },
                      "mpi": {
                              "file_patterns": {
                                                "pbs_stdout": ["Hello"]
                                               },
                              "files_exist": [],
                              "check_file_sizes": ["pbs_stderr"]
                             },
                      "java": {
                              "file_patterns": {
                                                "pbs_stdout": ["Hello Java"]
                                               },
                              "files_exist": [],
                              "check_file_sizes": []
                             },
                      "blas": {
                               "file_patterns": {
                                                 "pbs_stdout": ["SUM C =\s+45"]
                                                },
                               "files_exist": [],
                               "check_file_sizes": ["pbs_stderr"]
                              },
                      "boost": {
                                "file_patterns": {
                                                  "pbs_stdout": ["Working"]
                                                 },
                                "files_exist": [],
                                "check_file_sizes": ["pbs_stderr"]
                             },
                      "abaqus": {
                                 "file_patterns": {
                                                   "pbs_stdout": [
                                                                  "^Begin Abaqus/Standard Analysis$",
                                                                  "^End Abaqus/Standard Analysis$",
                                                                  "COMPLETED"
                                                                 ]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "R": {
# For generic apps, software name must match with the module name, "r" will not work. The software name is taken from the module name
# For other existing apps, the software names are harded coded in the class constructor, not necessary match the module names, but must math the key here! 
                                 "file_patterns": {
                                                   "pbs_stdout": [ "Hello R!"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },

                      "singularity": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["< moo >"] 
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },

                      "autodock": {
                                 "file_patterns": {
                                                   "pbs_stdout": [""]
                                                  },
                                 "files_exist": ["test-cases/autodock/1dwd_1dwd.dlg"],
                                 "check_file_sizes": []
                                },

                      "bcl2fastq": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["BCL to FASTQ file converter"] 
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "bcl2fastq2": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["BCL to FASTQ file converter"] 
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "fds": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["FDS completed successfully"]  #fds put info into stderr for some reasons
                                                  },
                                 "files_exist": ["test-cases/fds/create_remove.out"],
                                 "check_file_sizes": []
                                },
                      "fsl": {
                                 "file_patterns": {
                                                   "pbs_stdout": [""]
                                                  },
                                 "files_exist": ["test-cases/fsl/t1_seg.nii.gz"],
                                 "check_file_sizes": []
                                },
                      "geos": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["tests summary: ok:2051"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "glpk": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Model has been successfully processed"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "homer": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Finalizing Enrichment Statistics"]
                                                  },
                                 "files_exist": ["test-cases/homer/outputfile.txt"],
                                 "check_file_sizes": []
                                },
                      "columbus": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["end of argos"],
                                                   "test-cases/columbus/argosls": ["driver: overall argos workspace high-water mark =     46415"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "cellranger": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Pipestance completed successfully!"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "ls-dyna": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["initialization completed"]
# the job might be terminated by running time limit, but it will complete the initialization.
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "mathematica": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Mathematica"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "meep": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["finished at"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "miniconda": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Executing transaction: ...working... done"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "namd": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["END OF LOAD BALANCING"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "ncbi-blast": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Gap Penalties"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "ncbi-sratoolkit": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["284"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "openblas": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["test!"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "opensees": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["PASSED ALL TESTS","GM/ISE-WE OK"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "orca": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["ORCA TERMINATED NORMALLY"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "parallel": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["C"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "perl": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Hello, World!"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "salmon": {
                                 "file_patterns": {
                                                   "pbs_stdout": [""]
                                                  },
                                 "files_exist": ["test-cases/salmon/salmon_quant/quant.sf"],
                                 "check_file_sizes": []
                                },
                      "samtools": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["TAATTAAGTCTACAGAGCAACTA"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "sbt": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["test-cases/sbt/./test"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "scala3": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Hello, world!"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "spaceranger": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Pipestance completed successfully!"]
                                                  },
                                 "files_exist": ["test-cases/spaceranger/tiny-bcl/tiny-bcl.mri.tgz"],
                                 "check_file_sizes": []
                                },
                      "subread": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Test finished"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "trimgalore": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["100000 sequences processed in total"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "cmake": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Hello World!"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "gdal": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Band 4 Block=32x1 Type=Byte, ColorInterp=Alpha"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "gmp": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["100 \+ 50 => 150"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "harminv": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["2.554004e-15"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "hdf5": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["HDF5 Done"]
                                                  },
                                 "files_exist": ["test-cases/hdf5/dset.h5"],
                                 "check_file_sizes": []
                                },
                      "jpeglib": {
                                 "file_patterns": {
                                                   "pbs_stdout": [""]
                                                  },
                                 "files_exist": ["test-cases/jpeglib/test.jpg"],
                                 "check_file_sizes": []
                                },
                      "proj": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["3399483.80	752085.60"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "sqlite": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["tt.db r/w"]
                                                  },
                                 "files_exist": ["test-cases/sqlite/tt.db"],
                                 "check_file_sizes": []
                                },
                      "squashfs": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Creating 4.0 filesystem on test.sqsh"]
                                                  },
                                 "files_exist": ["test-cases/squashfs/test.sqsh"],
                                 "check_file_sizes": []
                                },
                      "tcl": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["hello world"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "tiff": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["Planar Configuration","PlanarConfig"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "valgrind": {
                                 "file_patterns": {
                                                   "pbs_stderr": ["Invalid write of size 4"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "xalt": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["XALT operation test: successful"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "yaml-cpp": {
                                 "file_patterns": {
                                                   "pbs_stdout": ["file: yes"]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "starccm": {
                                 "file_patterns": {
                                                   "pbs_stdout": [
                                                                  "^Configuring finished$",
                                                                  "^Saving:",
                                                                  "^Server process exited with code\s*:*\s+0$"
                                                                 ]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                                },
                      "vasp": {
                               "file_patterns": {
                                                 "OUTCAR": [
                                                            "aborting loop because EDIFF is reached",
                                                            "General timing and accounting informations for this job"
                                                           ]
                                                },
                               "files_exist": [],
                               "check_file_sizes": []
                              },
                      "matlab": {
                                 "file_patterns": {
                                                   "pbs_stdout": [
                                                                  "^e =$",
                                                                  "991$"
                                                                 ]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                              },
                      "m": {
                               "file_patterns": {
                                                 "pbs_stdout": [
                                                                "mcrun  is done$"
                                                               ]
                                                },
                               "files_exist": ["mcnp_o","mcnp_r","mcnp_s"],
                               "check_file_sizes": []
                           },
                      "x": {
                            "file_patterns": {
                                              "pbs_stdout": [
                                                             "mcrun  is done$"
                                                            ]
                                             },
                            "files_exist": ["mcnp_o","mcnp_r","mcnp_m"],
                            "check_file_sizes": []
                           },
                      "helios": {
                                 "file_patterns": {
                                                   "pbs_stdout": [
                                                                  "ZENITH Successful Completion"
                                                                 ]
                                                  },
                            "files_exist": [],
                            "check_file_sizes": ["pbs_stderr"]
                           },
                      "mc21": {
                            "file_patterns": {
                                              "pbs_stdout": [
                                                             "Simulation Completed",
                                                             "Number of errors:\s*0"
                                                            ]
                                             },
                            "files_exist": [],
                            "check_file_sizes": []
                           },
                      "scale": {
                                "file_patterns": {
                                                  "scale_out": [
                                                                "normal termination"
                                                               ]
                                                 },
                                "files_exist": [],
                                "check_file_sizes": []
                               },
                      "scale62": {
                                "file_patterns": {
                                                  "scale_out": [
                                                                "SCALE is finished"
                                                               ]
                                                 },
                                "files_exist": [],
                                "check_file_sizes": []
                               },
                      "serpent": {
                                  "file_patterns": {
                                                    "pbs_stdout": [
                                                                   "Transport cycle completed"
                                                                  ]
                                                   },
                                  "files_exist": ["serpent_out"],
                                  "check_file_sizes": []
                                 },
                      "gaussian": {
                                   "file_patterns": {
                                                     "gaussian_out": [
                                                                      "Normal termination of Gaussian"
                                                                     ]
                                                    },
                                   "files_exist": [],
                                   "check_file_sizes": []
                                  },
                      "cth": {
                              "file_patterns": {
                                                "pbs_stdout": [
                                                                 "CALCULATION TERMINATED BECAUSE STOP TIME ACHIEVED"
                                                              ]
                                               },
                              "files_exist": ["octh"],
                              "check_file_sizes": []
                             },
                      "lammps": {
                                 "file_patterns": {
                                                   "log.lammps": [
                                                                  "MPI task timing breakdown",
                                                                  "Total wall time"
                                                                 ]
                                                  },
                                 "files_exist": [],
                                 "check_file_sizes": []
                             },
                      "nwchem": {
                                 "file_patterns": {
                                                   "pbs_stdout": [
                                                                  "CITATION",
                                                                  "Total times  cpu"
                                                                 ]
                                                  },
                                 "files_exist": ["ecpchho.db"],
                                 "check_file_sizes": []
                             }
                     }


g_hostname = socket.gethostname()
#
if g_hostname == "falcon1" or g_hostname == "falcon2" or g_hostname == "falconpbs" or g_hostname == "service2":
   clustername = "falcon"
else:
   clustername = g_hostname


def concat_files(f1_name, f2_name, f_name):

#    print f1_name, f2_name, f_name
    f1 = open(f1_name, 'r')
    if os.path.exists(f2_name):
       f2 = open(f2_name, 'r')
    f  = open(f_name, 'w')

    f.write(f1.read())
    if os.path.exists(f2_name):
       f.write(f2.read())


def gaussian_html_link_str(str1, jobid, result):

    file_o = str1 + ".o" + jobid
    file_e = str1 + ".e" + jobid
    file_out2 = str1 + ".oe" + jobid
    file_out = re.split("/",file_out2)[-1]
    concat_files(file_o,file_e,file_out)
    result = "<a href=\"" + str1 + "\"" + "target=\"_blank\">" + result + "</a>"
    return result


def html_link_str(str1, jobid, result):
    file_o = str1 + ".o" + jobid
    file_e = str1 + ".e" + jobid
    file_out2 = str1 + ".oe" + jobid
    file_out = re.split("/",file_out2)[-1]
    concat_files(file_o,file_e,file_out)
    result = "<a href=\"" + clustername + "/" + file_out + "\"" + "target=\"_blank\">" + result + "</a>"
    return result


def log_link_str(hostname, file_str, result):
    shutil.copy(hostname + "_" + file_str + ".log", hostname + "_" + file_str + ".txt")
    link_str = "<a href=\"" + clustername + "/" + hostname + "_" + file_str + ".txt" + "\" target=\"_blank\">" + result + "</a>"
    return link_str


def find_result_counts(l):
    cnt_p = 0
    cnt_f = 0
    cnt_c = 0
    cnt_r = 0
    for e in l:
        if e:
           if e == "passed":
              cnt_p = cnt_p + 1
           elif e == "failed":
              cnt_f = cnt_f + 1
           elif e == "check":
              cnt_c = cnt_c + 1
           elif e == "running":
              cnt_r = cnt_r + 1
           else:
              print "Warning: Do not recognize the string,",e
    return cnt_p,cnt_f,cnt_c,cnt_r


def get_sw_result_totals(sw_dict):
    passed_r,failed_r,checked_r,running_r = find_result_counts(sw_dict["results"])
    passed_rr,failed_rr,checked_rr,running_rr = find_result_counts(sw_dict["run_results"])
    total_passed = passed_r + passed_rr
    total_failed = failed_r + failed_rr
    total_checked = checked_r + checked_rr
    total_running = running_r + running_rr
    total_tests = total_passed + total_failed + total_checked + total_running
    return total_tests,total_passed,total_failed,total_checked,total_running


def get_all_result_totals(report_dict):
    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_checked = 0
    total_running = 0
    for sw_name in report_dict:
        total_sw_tests,total_sw_passed,total_sw_failed,total_sw_checked,total_sw_running = get_sw_result_totals(report_dict[sw_name])
        total_tests = total_tests + total_sw_tests
        total_passed = total_passed + total_sw_passed
        total_failed = total_failed + total_sw_failed
        total_checked = total_checked + total_sw_checked
        total_running = total_running + total_sw_running
    return total_tests,total_passed,total_failed,total_checked,total_running


def print_report(run_date, hostname, report_dict):
    if len(sys.argv) > 1 and re.match("h",sys.argv[1]):
       gen_html = True
    else:
       gen_html = False
    if gen_html:
       print "<html>"
       print "<body>"
       print "<pre>"
    print "\nSoftware Quality Assurance Tests run on ",hostname," at",run_date
    for sw_name in report_dict:
#         print "sw_name=",sw_name
         print '\n{:#^142}\n'.format(sw_name + ' Tests')
         for module,compiler,result,pbs_jobid,dir_name,pbs_jobname,run_result in zip(report_dict[sw_name]["module_names"],report_dict[sw_name]["compiler_names"],report_dict[sw_name]["results"],report_dict[sw_name]["pbs_job_ids"],report_dict[sw_name]["dir_names"],report_dict[sw_name]["pbs_job_names"],report_dict[sw_name]["run_results"]):
#                print module,compiler,result,pbs_jobid,pbs_jobname,run_result
             if sw_name in compile_sw_l:
                if gen_html and re.search("failed$|check$",result):
                   link_str = log_link_str(hostname,sw_name+"_test",result)
                   print '{:<40}{:<10}{:-<80} {:<8}'.format(module,compiler,'Compile',link_str)
                else:
                   print '{:<40}{:<10}{:-<80} {:<8}'.format(module,compiler,'Compile',result)
                if gen_html and re.search("failed$|check$",run_result) and re.search("\d+",pbs_jobid):
                   link_str = html_link_str(pbs_jobname, pbs_jobid, run_result)
                   print '{:<40}{:<10}{:<4}{:-<76} {:<8}'.format(module,compiler,'Job',pbs_jobid,link_str)
                else:
                   print '{:<40}{:<10}{:<4}{:-<76} {:<8}'.format(module,compiler,'Job',pbs_jobid,run_result)
             elif sw_name in dir_sw_l:
                if gen_html and re.search("failed$|check$",run_result) and re.search("\d+",pbs_jobid):
                   link_str = html_link_str(dir_name+"/"+pbs_jobname, pbs_jobid, run_result)
                   print '{:<40}{:<20}{:-<70} {:<8}'.format(module,dir_name,pbs_jobid,link_str)
                else:
                   print '{:<40}{:<20}{:-<70} {:<8}'.format(module,dir_name,pbs_jobid,run_result)
             elif sw_name == "python2" or sw_name == "python3":
                if gen_html and re.search("failed$|check$",result):
                   link_str = log_link_str(hostname,sw_name+"_test",result)
                   print '{:<40}{:-<90} {:<8}'.format(module,compiler,link_str)
                else:
                   print '{:<40}{:-<90} {:<8}'.format(module,compiler,result)
             else:
                if gen_html and re.search("failed$|check$",run_result) and re.search("\d+",pbs_jobid):
                   link_str = html_link_str(pbs_jobname, pbs_jobid, run_result)
                   print '{:<40}{:-<90} {:<8}'.format(module,pbs_jobid,link_str)
                else:
                   print '{:<40}{:-<90} {:<8}'.format(module,pbs_jobid,run_result)
         total_sw_tests,total_sw_passed,total_sw_failed,total_sw_checked,total_sw_running = get_sw_result_totals(report_dict[sw_name])
         print '\n{:#<142}\n'.format("")
         print 'Total Number of {} Tests = {} (Passed = {} Failed = {} Checked = {} Running = {})'.format(sw_name,total_sw_tests,total_sw_passed,total_sw_failed,total_sw_checked,total_sw_running)
#         print '\n{:#<142}\n'.format("")
    total_tests,total_passed,total_failed,total_checked,total_running = get_all_result_totals(report_dict)
    print '\n{:#<142}\n'.format("")
    print 'Total Number of Tests = {} (Passed = {} Failed = {} Checked = {} Running = {})'.format(total_tests,total_passed,total_failed,total_checked,total_running)
    print '\n{:#<142}\n'.format("")

    if gen_html:
       print "</pre>"
       print "</body>"
       print "</html>"


def find_results_out_files():
    results_out_files = []
    for file in glob.glob('*_results.out'):
#        print file
        results_out_files.append(file)
    return results_out_files


def find_name(file_name):
    sw_name = None
#    s = re.search('[a-zA-Z0-9]+_([a-zA-Z0-9]+)_results.out',file_name)
# added - to handle file name with "-" in the middle, like ls-dyna
    s = re.search('[a-zA-Z0-9]+_([a-zA-Z0-9-]+)_results.out',file_name)
    if s is not None:
       sw_name = s.groups(0)[0]
    else:
       print "Error in finding sw_name" 
#    return s.groups(0)[0]
    return sw_name


def extract_sw_names(results_out_files):
    sw_names = []
    for file_name in results_out_files:
        sw_name = find_name(file_name)
        sw_names.append(sw_name)
    return sw_names 


def collect_results(f, sw_name):
    modules = []
    dlist1 = []
    dlist2 = []
    dlist3 = []
    pbs_job_ids = []
    for line in f:
#        print line,
        data = re.split("\s*",line.strip())
#        s = re.search("passed$|failed$|check$",line.strip())
        if len(data) > 1:
           modules.append(data[0])
           if len(data) == 2:
              dlist1.append(data[1])
           elif len(data) == 3:
              dlist1.append(data[1])
              dlist2.append(data[2])
           elif len(data) == 4:
              dlist1.append(data[1])
              dlist2.append(data[2])
              dlist3.append(data[3])
           else:
              print "Warning: Do not recognize the line, ",line
#           print "next line1=",f.next()
           if sw_name == "python2" or sw_name == "python3":
              pbs_job_ids.append(None)
              continue
           line2 = f.next()
           s2 = re.search('\d+',line2.strip())
           if s2 is not None:
              pbs_job_ids.append(s2.group())
           else:
              pbs_job_ids.append("not_run")
    return modules,dlist1,dlist2,dlist3,pbs_job_ids


def parse_arg(arg):
    len_arg = len(arg)
    if len_arg == 1:
       job_name = arg[0]
    elif len_arg == 2:
       dir_name = arg[0]
       job_name = arg[1]
    else:
       print "Warning: incorrect number of variable args passed,",arg
    return dir_name,job_name


def get_file_path(dir_name, file):
    if dir_name:
      file_path = os.path.join(dir_name, file) 
    else:
      file_path = file
    return file_path


def get_file_name(file, job_name, job_id):
    if file == "pbs_stdout":
       file_name = job_name + ".o" + job_id
    elif file == "pbs_stderr":
       file_name = job_name + ".e" + job_id
    elif file == "mcnp_o":
       file_name = job_name + ".o"
    elif file == "mcnp_r":
       file_name = job_name + ".r"
    elif file == "mcnp_s":
       file_name = job_name + ".s"
    elif file == "mcnp_m":
       file_name = job_name + ".m"
    elif file == "scale_out":
       file_name = job_name + ".out"
    elif file == "serpent_out":
       file_name = job_name + ".out"
    elif file == "gaussian_out":
       file_name = job_name + ".out"
    else:
       file_name = file
    return file_name


def check_file_patterns_found(file_pattern_d, dir_name, job_name, job_id):
    for file in file_pattern_d:
#        print job_name," file pattern ", file
        file_name = get_file_name(file, job_name, job_id)
        file_path = get_file_path(dir_name, file_name)
        try:
            f = open(file_path,"r")
#            print "file is ", file_path
        except IOError, e:
            print "Error: could not open file", e
            return False
        lines = f.readlines()
#if empty output file, return true, 
        if not lines:
#           print "empty line\n"
           return True
        for pattern in file_pattern_d[file]:
#            print "search for pattern.",pattern
            found = False
            for line in lines:
                if re.search(pattern,line) is not None:
#                   print "found pattern.",pattern
                   found = True
                   break
            if not found:
               break
    return found


def check_file_patterns_found_cnt(file_pattern_d, dir_name, job_name, job_id):
    for file in file_pattern_d:
        file_name = get_file_name(file, job_name, job_id)
        file_path = get_file_path(dir_name, file_name)
        f = open(file_path,"r")
        lines = f.readlines()
        for pattern in file_pattern_d[file]:
#            print "search for pattern.",pattern
            found = False
            cnt = 0
            run_result = "failed"
            for line in lines:
                s = re.findall(pattern,line)
                if s is not None:
#                   print "found pattern.",pattern
                   cnt = cnt + len(s)
                   found = True
            if cnt < NUM_MPI_PROCS:
               run_result = "check"
               break
            elif cnt == NUM_MPI_PROCS:
               run_result = "passed"
            elif not found:
               run_result = "failed"
               break
    return run_result


def check_files_exist(files_exist_l, dir_name, job_name, job_id):
    files_exist = True
    for file in files_exist_l:
        file_name = get_file_name(file, job_name, job_id)
        file_path = get_file_path(dir_name, file_name)
        if os.path.isfile(file_path):
           files_exist = True
#           print file_path,"----- file exists"
        else:
           files_exist = False
           break
    return files_exist


def check_files_size_nonzero(files_check_size_l, dir_name, job_name, job_id):
    files_size_nonzero = False
    for file in files_check_size_l:
        file_name = get_file_name(file, job_name, job_id)
        file_path = get_file_path(dir_name, file_name)
        if os.path.isfile(file_path):
           if os.path.getsize(file_path) > 0:
              files_size_nonzero = True
              break
        else:
           files_size_nonzero = True
           break
    return files_size_nonzero


def check_run_results_dirnames_jobnames_jobids(sw_name, dir_names, pbs_job_names, pbs_job_ids):
    run_results = []
    if sw_name == "python2" or sw_name == "python3":
       run_results = [None]*len(dir_names)
    else:
       for dir_name, pbs_job_name, pbs_job_id in zip(dir_names, pbs_job_names, pbs_job_ids):
#           print "pbs_job_id=",pbs_job_id
           if re.search('\d+',pbs_job_id.strip()) is not None:
              pbs_stdout_file = get_file_name("pbs_stdout", pbs_job_name, pbs_job_id)
#              print "pbs_stdout_file=",pbs_stdout_file
              pbs_stdout_filepath = get_file_path(dir_name, pbs_stdout_file)
#              print "pbs_stdout_filepath=",pbs_stdout_filepath
              if os.path.isfile(pbs_stdout_filepath): 
                 if check_file_patterns_found(check_file_patterns[sw_name]["file_patterns"], dir_name, pbs_job_name, pbs_job_id):
                    if sw_name == "mpi":
                       run_result = check_file_patterns_found_cnt(check_file_patterns[sw_name]["file_patterns"], dir_name, pbs_job_name, pbs_job_id)
                    else:
                       run_result = "passed"
#                       print sw_name, "--check_file_patterns_found=passed"
                    if check_files_size_nonzero(check_file_patterns[sw_name]["check_file_sizes"], dir_name, pbs_job_name, pbs_job_id):
#                       print "check_files_size_nonzero=check"
                       run_result = "check"
                    if not check_files_exist(check_file_patterns[sw_name]["files_exist"], dir_name, pbs_job_name, pbs_job_id):
#                       print sw_name,"--", check_file_patterns[sw_name]["files_exist"], "---check_files_exist=failed"
                       run_result = "failed"
                 else:
                    run_result = "failed"
              else:
                 run_result = "running"
           else:
              run_result = "failed"
           run_results.append(run_result)
    return run_results


def get_compilernames_dirnames_jobnames_results(sw_name, dlist1, dlist2, dlist3):
    compiler_names = []
    dir_names = []
    pbs_job_names = []
    results = []
    if sw_name in compile_sw_l:
       compiler_names = dlist1
       dir_names = [None]*len(dlist1)
       pbs_job_names = dlist2
       results = dlist3
    elif sw_name in dir_sw_l:
       compiler_names = [None]*len(dlist1)
       dir_names = dlist1
       pbs_job_names = dlist2
       results = [None]*len(dlist2)
    elif sw_name == "python2" or sw_name == "python3":
       compiler_names = dlist1
       dir_names = [None]*len(dlist1)
       pbs_job_names = [None]*len(dlist1)
       results = dlist2
    else:
       compiler_names = [None]*len(dlist1)
       dir_names = [None]*len(dlist1)
       pbs_job_names = dlist1
       results = [None]*len(dlist1)
#       print "Warning: Do not know what to do with the following software,",sw_name
    return compiler_names, dir_names, pbs_job_names, results


def check_run_results(sw_name, dir_names, pbs_job_names, pbs_job_ids):
    run_results = check_run_results_dirnames_jobnames_jobids(sw_name, dir_names, pbs_job_names, pbs_job_ids)
    return run_results


def update_report_dict(report_dict, sw_name, module_names, compiler_names, dir_names, pbs_job_names, pbs_job_ids, results, run_results):
    if sw_name not in report_dict:
       report_dict[sw_name] = {}
       report_dict[sw_name]["module_names"] = module_names
       report_dict[sw_name]["compiler_names"] = compiler_names
       report_dict[sw_name]["dir_names"] = dir_names
       report_dict[sw_name]["pbs_job_names"] = pbs_job_names
       report_dict[sw_name]["pbs_job_ids"] = pbs_job_ids
       report_dict[sw_name]["results"] = results
       report_dict[sw_name]["run_results"] = run_results
    return report_dict


def get_dateHost():
    f = open("datehost.out", "r")
    lines = f.readlines()
    date = lines[0].strip()
    host = lines[1].strip()
    return date,host


def main():
    report_dict = {}
    run_date,run_hostname = get_dateHost()
    results_out_files = find_results_out_files()
#    print "results_out_files=",results_out_files
    sw_names = extract_sw_names(results_out_files)
#    print "sw_names =",sw_names
    for results_out_file in results_out_files:
#        print "results_out_file=",results_out_file
        sw_name = find_name(results_out_file)
        f = open(results_out_file, "r")
        modules,dlist1,dlist2,dlist3,pbs_job_ids = collect_results(f, sw_name)
        compiler_names, dir_names, pbs_job_names, results = get_compilernames_dirnames_jobnames_results(sw_name, dlist1, dlist2, dlist3)
        run_results = check_run_results(sw_name,dir_names,pbs_job_names,pbs_job_ids) 
#        print "run_results=",run_results
        report_dict = update_report_dict(report_dict, sw_name, modules, compiler_names, dir_names, pbs_job_names, pbs_job_ids, results, run_results)
#    print "report_dict=",report_dict
    print_report(run_date,run_hostname,report_dict)


if __name__ == '__main__':
    main()
