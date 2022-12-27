import time
import os
import queue
import sys
import json
import argparse
import datetime
import multiprocessing
from collections import OrderedDict
from constraint import *
from morph import flatten, unflatten

TS_G_PROGRESS = "Progress"
TS_G_STATUS = "Status"
TS_G_STATUS_N_A = "Idle"
TS_G_STATUS_RUNNING = "Running"
TS_G_STATUS_DONE = "Done"
TS_G_STATUS_TERMINATED = "Terminated"
TS_G_STATUS_ITER_DONE = "Iteration-done"


class CG_constraint_solver():

    def __init__(self):
        self.flat_dflt_config_d = {}
        self.nonflat_dflt_config_d = {}
        self.flat_domain_d = {}
        self.cg_root_config_d = {}
        self.cg_func_dict = {}
        self.cg_cnstr_dict = {}
        self.fdeflist = []
        self.tot_num_of_combinations = 1
        self.cfg_counter = 0
        self.problem = None

    def read_cg_root_json(self, _dir, main_cfg):
        cg_root_json_path = os.path.join(_dir, "root.json")
        cg_root_json_path = os.path.join(_dir, main_cfg)

        try:
            with open(cg_root_json_path) as _f:
                _cg_cfg = json.loads(_f.read())
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Decoding JSON has failed - %s' % cg_root_json_path)
            return False
        except:
            print ('File open faild - %s' % cg_root_json_path)
            return False

        self.cg_root_config_d = _cg_cfg
        return True

    def get_flatten_default_config(self, _dir):
        cg_dflt_json_path = os.path.join(_dir, self.cg_root_config_d["default_config"])

        try:
            with open(cg_dflt_json_path) as _f:
                _dflt_cfg = json.loads(_f.read(), object_pairs_hook=OrderedDict)

        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Decoding JSON has failed - %s' % cg_dflt_json_path)
            return False
        except:
            print ('File open failed - %s' % cg_dflt_json_path)
            return False

        self.nonflat_dflt_config_d = _dflt_cfg
        self.flat_dflt_config_d = flatten(_dflt_cfg)
        #       print self.flat_dflt_config_d
        return True

    def get_flatten_domain_dict(self, _dir):
        cg_domain_json_path = os.path.join(_dir, self.cg_root_config_d["domain_config"])

        try:
            with open(cg_domain_json_path) as _f:
                _cg_domain_cfg = json.loads(_f.read())

        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Decoding JSON has failed - %s' % cg_domain_json_path)
            return False
        except:
            print ('File open failed - %s' % cg_domain_json_path)
            return False

        self.flat_domain_d = flatten(_cg_domain_cfg)
        #    print self.flat_domain_d
        return True

    def get_func_dict(self, _dir):
        cg_func_json_path = os.path.join(_dir, self.cg_root_config_d["constraints_functions"])

        try:
            with open(cg_func_json_path) as _f:
                _cg_func_const_dict = json.loads(_f.read())

        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Decoding JSON has failed - %s' % cg_func_json_path)
            return False
        except:
            print ('File open failed - %s' % cg_func_json_path)
            return False

        self.cg_func_dict = _cg_func_const_dict["functions"]
        self.cg_cnstr_dict = _cg_func_const_dict["constraints"]

        print (self.cg_func_dict)
        print (self.cg_cnstr_dict)

        for _k, _v in self.cg_func_dict.items():
            _bld = "def " + _k + "(" + _v["param"] + ")" + ": " + _v["body"]
            self.fdeflist.append(_bld)

        # print self.fdeflist
        return True

    def merge_solution_into_default_base(self, _sol, _base):
        for _k, _v in _sol.items():
            _base[_k] = _v

        return _base

    def go(self, status_q, cmd_q, in_dir, log_file, sol_file, main_cfg):
        prv_out_dir = None
        # read json configs set of files
        if (not self.read_cg_root_json(in_dir, main_cfg)) or \
                (not self.get_flatten_default_config(in_dir)) or \
                (not self.get_flatten_domain_dict(in_dir)) or \
                (not self.get_func_dict(in_dir)):
            full_stat = {TS_G_STATUS: TS_G_STATUS_TERMINATED}
            status_q.put(full_stat)
            return

        self.problem = Problem()
        for _k, _v in self.flat_domain_d.items():
            print( ">>>>>> going to evaluate %s %s \n" %(_k, _v))
            self.problem.addVariable(_k, eval(_v))
            self.tot_num_of_combinations *= float(len(eval(_v)))

        print("tot_num_of_combinations before applying restrictions: %g" % self.tot_num_of_combinations)

        # Make constraint functions acquainted of the rest of the code
        for _fdef in self.fdeflist:
            exec (_fdef)

        for _i in range(len(self.cg_cnstr_dict)):
            print(self.cg_cnstr_dict[_i])
            _f = self.cg_cnstr_dict[_i][0]
            _l = self.cg_cnstr_dict[_i][1]
            self.problem.addConstraint(eval(_f),_l)
        self.iter = self.problem.getSolutionIter()

        while True:
            time.sleep(0.001)

            try:
                out_dir = cmd_q.get_nowait()
                if prv_out_dir == out_dir:
                    continue    # not likely to happen
                prv_out_dir = out_dir
                self.cfg_counter += 1

                _solution_d = self.iter.__next__()
#                merged_cfg_d = self.merge_solution_into_default_base(_solution_d, self.flat_dflt_config_d)

#                print (_solution_d)
#                print (merged_cfg_d)
                print(self.cfg_counter)

                with open(log_file, 'a') as _f:
                    if self.cfg_counter == 1:
                        _f.write("{ \n")
                    else:
                        _f.write(", \n")

                    _f.write("\"solution_%d\": " %self.cfg_counter )
                    json.dump(_solution_d, _f, indent=4)

#                merged_cfg_d = unflatten(merged_cfg_d)
#                _cg_cfg_path = os.path.join(out_dir, "cg_cfg.json")
#                with open(_cg_cfg_path, 'w') as _f:
#                    json.dump(merged_cfg_d, _f, indent=4)

                full_stat = {TS_G_STATUS: TS_G_STATUS_ITER_DONE}
                status_q.put(full_stat)

            except queue.Empty:
                pass

            except StopIteration:
                break

        # Should reach here only when all configs are generated and none is left

        with open(log_file, 'a') as _f:     # wrap up JSONized log file
                _f.write("\n} \n")

        full_stat = {TS_G_STATUS: TS_G_STATUS_DONE}
        status_q.put(full_stat)

        self.restore_identifiers(log_file, sol_file)
        return

    def restore_identifiers(self, log_file, sol_file):

        try:
            with open(log_file) as _f:
                all_configs_d = json.loads(_f.read(), object_pairs_hook=OrderedDict)

        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Decoding JSON has failed - %s' % log_file)
            return False
        except:
            print ('File open failed - %s' % log_file)
            return False

        for _ks, _vs in self.nonflat_dflt_config_d["legend"].items():
            for _kd, _vd in all_configs_d.items():
                if _ks in _vd:
                    _vd[_ks] = _vs[str(_vd[_ks])]

        with open(sol_file, 'w') as _f:
            json.dump(all_configs_d, _f, indent=4)

    def get_solution(self, _in_dir, _main_cfg):
        # read json configs set of files
        if (not self.read_cg_root_json(_in_dir, _main_cfg)) or \
                (not self.get_flatten_default_config(_in_dir)) or \
                (not self.get_flatten_domain_dict(_in_dir)) or \
                (not self.get_func_dict(_in_dir)):
            return

        self.problem = Problem()
        for _k, _v in self.flat_domain_d.items():
            print(">>>>>> going to evaluate %s %s \n" % (_k, _v))
            self.problem.addVariable(_k, eval(_v))
            self.tot_num_of_combinations *= float(len(eval(_v)))

        print("tot_num_of_combinations before applying restrictions: %g" % self.tot_num_of_combinations)

        # Make constraint functions acquainted of the rest of the code
        for _fdef in self.fdeflist:
            exec(_fdef)

        for _i in range(len(self.cg_cnstr_dict)):
            print(self.cg_cnstr_dict[_i])
            _f = self.cg_cnstr_dict[_i][0]
            _l = self.cg_cnstr_dict[_i][1]
            self.problem.addConstraint(eval(_f), _l)
        return self.problem.getSolutions()


def obtain_main_class():
    a = CG_constraint_solver()
    return a


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Constraint solver script")
    parser.add_argument("config_path", metavar="config_path", type=str,
                        help="Path to the main configuration (.json) file.")

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    args = parser.parse_args()
    main_cfg = args.config_path
    print("main_cfg is {0} \n".format(main_cfg))

#    with open(args.config_path) as src:
#        main_cfg = json.loads(src.read())

    time_out_per_iteration = 20
    out_subdir = None
    cfgs_lim = 100000
    in_dir = "\\"
    subdir_enumerator = 0

    base_wd = ".\\workdir"

    _dtag = datetime.datetime.now().strftime("test_root_%y_%m_%d_%H_%M_%S")
    test_work_dir = os.path.join(base_wd, _dtag)
    os.makedirs(test_work_dir)

    logf = os.path.join(test_work_dir, "log.json")
    solf = os.path.join(test_work_dir, "solutions.json")

    status_q = multiprocessing.Queue()
    cmd_q = multiprocessing.Queue()

    cg_class_object = CG_constraint_solver()

    cg_p = multiprocessing.Process(target=cg_class_object.go, args=(status_q, cmd_q, in_dir, logf, solf, main_cfg))
    cg_p.start()

    while True:
        subdir_enumerator += 1
        out_subdir = ".\\out"
        out_dir = os.path.join(test_work_dir, str(subdir_enumerator), out_subdir)
#        if not os.path.exists(out_dir):
#            os.makedirs(out_dir)

#        print ("out_dir: %s" % out_dir)

        count_down = time_out_per_iteration

        # Check if num of configs limit has been met
        cfgs_lim -= 1
        if cfgs_lim < 0:
            cg_p.terminate()
            cg_p.join()
            sys.exit(0)

        cmd_q.put(out_dir)

        while count_down > 0:
            count_down -= 1
            time.sleep(0.001)

            try:
                ret_stat = status_q.get_nowait()
                if ret_stat[TS_G_STATUS] == TS_G_STATUS_DONE:
                    if cg_p.is_alive():
                        cg_p.join()
                    sys.exit(0)

                if ret_stat[TS_G_STATUS] == TS_G_STATUS_ITER_DONE:
                    break

                if ret_stat[TS_G_STATUS] == TS_G_STATUS_TERMINATED:
                    cg_p.terminate()
                    cg_p.join()
                    sys.exit(1)

            except queue.Empty:
                continue

