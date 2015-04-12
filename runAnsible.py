import ansible.runner
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils


stats = callbacks.AggregateStats()
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

inven = Inventory(host_list='ansible/hosts');

pb = PlayBook(inventory=inven,playbook='ansible/main.yml',stats=stats,callbacks=playbook_cb,runner_callbacks=runner_cb,)
pb.run()
