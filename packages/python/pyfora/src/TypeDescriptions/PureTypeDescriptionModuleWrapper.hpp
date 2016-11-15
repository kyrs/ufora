/***************************************************************************
   Copyright 2016 Ufora Inc.

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
#pragma once

#include <Python.h>

class FileTypeDescription;

class PureTypeDescriptionModuleWrapper {
public:
    static PyObject* pyHomogeneousListAsNumpyArray(const PyObject*);
    static PyObject* pyFileDescription(const FileTypeDescription&);
private:
    static PureTypeDescriptionModuleWrapper& _getInstance()
        {
        static PureTypeDescriptionModuleWrapper singleton;
        return singleton;
        }

    PureTypeDescriptionModuleWrapper();

    PureTypeDescriptionModuleWrapper(
        const PureTypeDescriptionModuleWrapper&
        ) = delete;
    void operator=(PureTypeDescriptionModuleWrapper&) = delete;

    PyObject* mPureTypeDescriptionModule;
};