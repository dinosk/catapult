// Copyright (c) 2016 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
'use strict';

var fs = require('fs');
var path = require('path');

var catapultPath = fs.realpathSync(path.join(__dirname, '..', '..'));
var catapultBuildPath = path.join(catapultPath, 'catapult_build');

var node_bootstrap = require(path.join(catapultBuildPath, 'node_bootstrap.js'));

HTMLImportsLoader.addArrayToSourcePath(
    node_bootstrap.getSourcePathsForProject('lighthouse'));

// Go!
HTMLImportsLoader.loadHTML('/lighthouse/lighthouse.html');

// Make the lh namespace the main lighthouse export.
module.exports = global.lh;
