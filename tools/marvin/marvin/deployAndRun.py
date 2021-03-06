# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import deployDataCenter
import TestCaseExecuteEngine
import sys
from argparse import ArgumentParser
if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("-d", "--directory", dest="testCaseFolder",
                        help="the test case directory")
    parser.add_argument("-f", "--file", dest="module",
                        help="run tests in the given file")
    parser.add_argument("-r", "--result", dest="result",
                        help="test result log file", default='/tmp/t.log')
    parser.add_argument("-t", "--client", dest="testcaselog",
                        help="test case log file", default='/tmp/r.log')
    parser.add_argument("-c", "--config", action="store",
                        default="./datacenterCfg", dest="config",
                        help="the path where the json config file generated,\
 by default is ./datacenterCfg")
    parser.add_argument("-l", "--load", dest="load", action="store_true",
                        help="only load config, do not deploy,\
 it will only run testcase")
    parser.add_argument("-n", "--num", dest="number",
                        help="how many times you want run the test case")

    options = parser.parse_args()

    testResultLogFile = None
    if options.result is not None:
        testResultLogFile = options.result

    testCaseLogFile = None
    if options.testcaselog is not None:
        testCaseLogFile = options.testcaselog
    deploy = deployDataCenter.deployDataCenters(options.config)
    if options.load:
        deploy.loadCfg()
    else:
        deploy.deploy()
    iterates = 1
    if options.number is not None:
        if options.number == "loop":
            iterates = sys.maxint
        else:
            try:
                iterates = int(options.number)
            except:
                iterates = 1

    if options.testCaseFolder is None:
        if options.module is None:
            parser.print_usage()
            exit(1)
        else:
            n = 0
            while(n < iterates):
                engine = \
                    TestCaseExecuteEngine.TestCaseExecuteEngine(
                        deploy.testClient,
                        deploy.getCfg(
                        ),
                        testCaseLogFile,
                        testResultLogFile)
                engine.loadTestsFromFile(options.module)
                engine.run()
                n = n + 1
    else:
        n = 0
        while(n < iterates):
            engine = TestCaseExecuteEngine.TestCaseExecuteEngine(
                deploy.testClient,
                deploy.getCfg(
                ),
                testCaseLogFile,
                testResultLogFile)
            engine.loadTestsFromDir(options.testCaseFolder)
            engine.run()
            n = n + 1
