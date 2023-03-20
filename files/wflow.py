from fireworks.core.firework import Firework, Workflow
from workflow.tasks import SAPT

    
def SAPTWorkflow(identifier, xyz, label):

    f1 = Firework(SAPT(identifier=identifier, xyz=xyz, label=label))
  
    wf = Workflow([f1], name="SAPTWorkflow")
  
    return wf
