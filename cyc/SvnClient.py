from  subprocess import Popen, PIPE  # replaces popen*()
                                     # see http://www.python.org/dev/peps/pep-0324/


# svn bump 2
Quote=lambda s: "'"+s+"'"

SvnCmd = "/usr/bin/svn"
UserFlag = "--username"
MessageFlag = "-m"

Cat = lambda l: " ".join(l)

class SvnClient():

    def __init__(self, path, user=None):
        '''
        Pre: path = path to working copy
        '''
        
        self.path = path
        self.user = user

        self.out = ""
        self.err = ""
 
    def GetUserArg(self):

        rv = ""
        if self.user != None:
            rv = Cat[UserFlag,self.user]
        return rv


    def Exec(self, cmd, *cmdargs):

        cmd = [SvnCmd, cmd, self.path]
        cmd.extend(*cmdargs)

        print cmd
    
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, close_fds=True)
        self.out = p.stdout.read()
        self.err = p.stderr.read()

    def Commit(self, message="no message"):

        args = [MessageFlag, message]
        self.Exec("commit",args)


    def Update(self):

        self.Exec("update")

        
   
