# $HeadURL$
__RCSID__ = "$Id$"

import time
import random
from DIRAC import S_OK, S_ERROR, gLogger, gConfig
from DIRAC.Core.DISET.RPCClient import RPCClient
from DIRAC.Core.Utilities.ThreadSafe import Synchronizer
from DIRAC.RequestManagementSystem.Client.RequestContainer import RequestContainer
from DIRAC.RequestManagementSystem.Client.RequestClient import RequestClient

gAccountingSynchro = Synchronizer()
random.seed()

class DataStoreClient:


  def __init__( self, setup = False, retryGraceTime = 0 ):
    self.__setup = setup
    self.__maxRecordsInABundle = 100
    self.__registersList = []
    self.__maxTimeRetrying = retryGraceTime
    self.__lastSuccessfulCommit = time.time()
    self.__failoverEnabled = True

  def setRetryGraceTime( self, retryGraceTime ):
    self.__maxTimeRetrying = retryGraceTime

  def __checkBaseType( self, obj ):
    """
    Check to find that the class inherits from the Base Type
    """
    for parent in obj.__bases__:
      if parent.__name__ == "BaseAccountingType":
        return True
      if self.__checkHandler( parent ):
        return True
    return False

  @gAccountingSynchro
  def addRegister( self, register ):
    """
    Add a register to the list to be sent
    """
    if not self.__checkBaseType( register.__class__ ):
      return S_ERROR( "register is not a valid type (has to inherit from BaseAccountingType" )
    retVal = register.checkValues()
    if not retVal[ 'OK' ]:
      return retVal
    if gConfig.getValue( '/LocalSite/DisableAccounting', False ):
      return S_OK()
    self.__registersList.append( register.getValues() )
    return S_OK()

  def disableFailover( self ):
    self.__failoverEnabled = False

  def __getRPCClient( self ):
    if self.__setup:
      return RPCClient( "Accounting/DataStore", setup = self.__setup, timeout = 3600 )
    return RPCClient( "Accounting/DataStore", timeout = 3600 )

  @gAccountingSynchro
  def commit( self ):
    """
    Send the registers in a bundle mode
    """
    rpcClient = self.__getRPCClient()
    sent = 0
    while len( self.__registersList ) > 0:
      registersToSend = self.__registersList[ :self.__maxRecordsInABundle ]
      retVal = rpcClient.commitRegisters( registersToSend )
      if retVal[ 'OK' ]:
        self.__lastSuccessfulCommit = time.time()
      else:
        if self.__failoverEnabled and time.time() - self.__lastSuccessfulCommit > self.__maxTimeRetrying:
          gLogger.verbose( "Sending accounting records to failover" )
          result = self.__sendToFailover( retVal[ 'rpcStub' ] )
          if not result[ 'OK' ]:
            return result
        else:
          return S_ERROR( "Cannot commit data to DataStore service" )
      sent += len( registersToSend )
      del( self.__registersList[ :self.__maxRecordsInABundle ] )
    return S_OK( sent )

  def __sendToFailover( self, rpcStub ):
    requestClient = RequestClient()
    request = RequestContainer()
    request.setDISETRequest( rpcStub )

    requestStub = request.toXML()['Value']
    return requestClient.setRequest( "Accounting.DataStore.%s.%s" % ( time.time(), random.random() ),
                                     requestStub )

  def remove ( self, register ):
    if not self.__checkBaseType( register.__class__ ):
      return S_ERROR( "register is not a valid type (has to inherit from BaseAccountingType" )
    retVal = register.checkValues()
    if not retVal[ 'OK' ]:
      return retVal
    if gConfig.getValue( '/LocalSite/DisableAccounting', False ):
      return S_OK()
    return self.__getRPCClient().remove( register.getValues() )

gDataStoreClient = DataStoreClient()
