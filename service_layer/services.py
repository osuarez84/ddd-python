from model import OrderLine
from repository import AbstractRepository
import model


/###############################
# Service layer / use-case layer
################################
# Service-layer services
# All the orchestration logic lives in this layer

class InvalidSku(Exception):
  pass


def is_valid_sku(sku, batches):
  return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
  # Get list of batches from repository
  batches = repo.list()

  # Check if sku from orderline is valid
  if not is_valid_sku(line.sku, batches):
    raise InvalidSku(f'Invalid sku {line.sku}')
  
  # if valid, try to allocate calling the domain service
  batchref = model.allocate(line, batches)

  # everything fine, save 
  session.commit()

  # return the reference of the batch to which the orderline has been allocated
  return batchref