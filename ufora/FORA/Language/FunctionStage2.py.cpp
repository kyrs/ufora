/***************************************************************************
   Copyright 2015 Ufora Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
****************************************************************************/
#include "FunctionStage2.hppml"

#include "../../core/python/ValueLikeCPPMLWrapper.hppml"
#include <boost/python.hpp>
#include "../../native/Registrar.hpp"
#include "../../core/python/CPPMLWrapper.hpp"
#include "FunctionStage2.hppml"

class FunctionStage2Wrapper :
		public native::module::Exporter<FunctionStage2Wrapper> {
public:
		std::string	     getModuleName(void)
			{
			return "FORA";
			}

		void exportPythonWrapper()
			{
			using namespace boost::python;

			ValueLikeCPPMLWrapper::exposeValueLikeCppmlType<FunctionStage2::Function>();
			ValueLikeCPPMLWrapper::exposeValueLikeCppmlType<FunctionStage2::Expression>();
			}
};

//explicitly instantiating the registration element causes the linker to need
//this file
template<>
char native::module::Exporter<FunctionStage2Wrapper>::mEnforceRegistration =
		native::module::ExportRegistrar<
			FunctionStage2Wrapper>::registerWrapper();






