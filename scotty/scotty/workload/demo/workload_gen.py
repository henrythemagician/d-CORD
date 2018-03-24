import logging
import time
import paramiko
from scotty import utils

logger = logging.getLogger(__name__)


def run(context):
    workload = context.v1.workload
    experiment_helper = utils.ExperimentHelper(context)
    demo_resource = experiment_helper.get_resource(
        workload.resources['demo_res'])
    iterations = workload.params['iterations']
    sleep_in_sec = workload.params['sleep']
    logger.info('{}'.format(workload.params['greeting']))
    logger.info('I\'m workload generator {}'.format(workload.name))
    logger.info('Resource endpoint: {}'.format(demo_resource.endpoint))
    myconn = paramiko.SSHClient()
    myconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    myconn.connect('10.1.0.2', port=22, username='cloud',
                   password='Sendate2017', look_for_keys=False, allow_agent=False)
    myshell = myconn.invoke_shell()
    for i in range(0, iterations):
        logger.info('Iteration: {}'.format(i))
        if workload.name == "iperf3_test":

            shell_cmd = ' iperf3  -c  10.6.3.101 -u -b 0 -l %s -n 1000000000 -V -J | tee results/test_result_%s.json  \n' % (
                str(1000 + 100 * i), str(i + 1))
            myshell.send(shell_cmd)
    #        output = myshell.recv(65535)
    #        logger.info(output)

    #        mystr = output.decode(encoding='UTF-8')
    #        logger.info(mystr)
        time.sleep(sleep_in_sec)
    myconn.close()
    result = 'result'
    return result


def collect(context):
    logger.info('collect data from workload')
    workload_utils = utils.WorkloadUtils(context)
    with workload_utils.open_file('my_result_file.txt', 'a') as f:
        f.write('result 1\n')
        f.write('result 2\n')


def clean(context):
    workload = context.v1.workload
    logger.info('I\'m workload cleaner {}'.format(workload.name))
    pass
