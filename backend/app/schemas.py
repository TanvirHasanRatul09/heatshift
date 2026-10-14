from pydantic import BaseModel, Field


class WhatIfRequest(BaseModel):
    transfer_locked: bool = Field(default=False, description="Whether fabric-roll transfer is unavailable for movement")
