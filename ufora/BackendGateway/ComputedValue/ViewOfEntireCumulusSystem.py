#   Copyright 2015 Ufora Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import ufora.BackendGateway.ComputedGraph.ComputedGraph as ComputedGraph
import ufora.native.Cumulus as CumulusNative
import ufora.native.FORA as ForaNative
import ufora.BackendGateway.ComputedValue.ComputedValueGateway as ComputedValueGateway
import time
import ufora.BackendGateway.ComputedGraph.BackgroundUpdateQueue as BackgroundUpdateQueue

getGateway = ComputedValueGateway.getGateway

class ViewOfEntireCumulusSystem(ComputedGraph.Location):
    viewOfSystem_ = ComputedGraph.Mutable(object, lambda: ())
    recentGlobalUserFacingLogMessages_ = ComputedGraph.Mutable(object, lambda: ())
    totalMessageCountsEver_ = ComputedGraph.Mutable(object, lambda: 0)

    @ComputedGraph.ExposedProperty()
    def mostRecentMessages(self):
        return self.recentGlobalUserFacingLogMessages_

    @ComputedGraph.ExposedProperty()
    def totalMessagesEver(self):
        return self.totalMessageCountsEver_

    @ComputedGraph.ExposedFunction()
    def clearMostRecentMessages(self, arg):
        self.recentGlobalUserFacingLogMessages_ = ()

    @ComputedGraph.ExposedFunction()
    def clearAndReturnMostRecentMessages(self, arg):
        messages = self.recentGlobalUserFacingLogMessages_
        self.recentGlobalUserFacingLogMessages_ = ()
        return messages

    @ComputedGraph.ExposedProperty()
    def viewOfCumulusSystem(self):
        return self.viewOfSystem_

    @ComputedGraph.ExposedFunction()
    def pushNewGlobalUserFacingLogMessage(self, msg):
        self.totalMessageCountsEver_ = self.totalMessageCountsEver_ + 1
        self.recentGlobalUserFacingLogMessages_ = (
            self.recentGlobalUserFacingLogMessages_ + \
                ({"timestamp": msg.timestamp, "message": msg.message, "isDeveloperFacing": msg.isDeveloperFacing, },)
            )



