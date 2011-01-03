# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# File modified for PLD Linux.
# Sets minimal configs necessary to run cassandra and cassandra CLI from 
# /usr/share/cassandra/*.jar
# Should easily allow to run multibple cassandra instaces by only providing
# $CASSANDRA_HOME

if [ "x$CASSANDRA_HOME" = "x" ]; then
    CASSANDRA_HOME=/var/lib/cassandra
fi

# The directory where Cassandra's configs live (required)
if [ "x$CASSANDRA_CONF" = "x" ]; then
    CASSANDRA_CONF=$CASSANDRA_HOME/conf
fi

# This can be the path to a jar file, or a directory containing the 
# compiled classes. NOTE: This isn't needed by the startup script,
# it's just used here in constructing the classpath.
# cassandra_bin=$CASSANDRA_HOME/build/classes
# cassandra_bin=/usr/share/cassandra

# JAVA_HOME can optionally be set here
#JAVA_HOME=/usr/local/jdk6

# The java classpath (required)
CLASSPATH=$CASSANDRA_CONF # :$cassandra_bin

# for jar in $CASSANDRA_HOME/lib/*.jar; do
#    CLASSPATH=$CLASSPATH:$jar
# done

# for jar in /usr/share/cassandra/*.jar; do
#     CLASSPATH=$CLASSPATH:$jar
# done
CLASSPATH=$CLASSPATH:/usr/share/cassandra/*:/usr/share/java/*

