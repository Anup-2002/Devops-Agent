from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from autoops_ai.db.models import DeploymentStatus, IncidentSeverity, UserRole


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)


class OrganizationRead(BaseModel):
    id: int
    name: str


class TeamCreate(BaseModel):
    organization_id: int
    name: str = Field(min_length=2, max_length=255)


class TeamRead(BaseModel):
    id: int
    organization_id: int
    name: str


class UserCreate(BaseModel):
    organization_id: int
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    role: UserRole = UserRole.MEMBER


class UserRead(BaseModel):
    id: int
    organization_id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool


class AgentCreate(BaseModel):
    team_id: int
    name: str = Field(min_length=2, max_length=255)
    configuration: dict = Field(default_factory=dict)


class AgentRead(BaseModel):
    id: int
    team_id: int
    name: str
    configuration: dict


class DeploymentCreate(BaseModel):
    organization_id: int
    agent_id: int | None = None
    environment: str = Field(min_length=2, max_length=64)


class DeploymentRead(BaseModel):
    id: int
    organization_id: int
    agent_id: int | None
    environment: str
    status: DeploymentStatus


class DeploymentRunRead(BaseModel):
    id: int
    deployment_id: int
    triggered_by_user_id: int | None
    status: DeploymentStatus
    started_at: datetime | None
    completed_at: datetime | None


class IncidentCreate(BaseModel):
    organization_id: int
    deployment_id: int | None = None
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    severity: IncidentSeverity


class IncidentRead(BaseModel):
    id: int
    organization_id: int
    deployment_id: int | None
    title: str
    description: str
    severity: IncidentSeverity
    resolved: bool


class RCAReportRead(BaseModel):
    id: int
    incident_id: int
    root_cause: str
    impact_assessment: str
    timeline: dict


class MetricRead(BaseModel):
    id: int
    deployment_id: int | None
    metric_name: str
    metric_value: float
    labels: dict


class AlertRead(BaseModel):
    id: int
    monitoring_metric_id: int
    deployment_id: int | None
    threshold: float
    current_value: float
    is_resolved: bool


class GitCommitRead(BaseModel):
    id: int
    deployment_run_id: int | None
    commit_sha: str
    message: str
    author_email: EmailStr


class PullRequestRead(BaseModel):
    id: int
    git_commit_id: int | None
    external_id: str
    title: str
    state: str


class TestResultRead(BaseModel):
    id: int
    deployment_run_id: int
    suite_name: str
    passed: bool
    total_tests: int
    failed_tests: int


class AuditLogRead(BaseModel):
    id: int
    organization_id: int
    user_id: int | None
    action: str
    resource_type: str
    resource_id: str
    metadata: dict
    created_at: datetime
