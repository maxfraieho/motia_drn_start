# Template Method Pattern для Motia Steps

## Pattern Overview

Template Method Pattern визначає скелет алгоритму в базовому методі, дозволяючи підкласам перевизначати окремі кроки алгоритму без зміни його структури.

## Motia-Specific Implementation

В Motia це реалізується через:
1. **Shared utility functions** - базовий алгоритм
2. **Configuration-driven behavior** - варіації через config
3. **Middleware** - template з customizable steps (для API)

## Key Concepts

1. **Fixed Algorithm**: Основна послідовність незмінна
2. **Customizable Steps**: Окремі кроки можна змінювати
3. **Hooks**: Точки розширення в алгоритмі
4. **Reusability**: Загальний код в одному місці

## Code Structure - Shared Template

```typescript
// Template function (shared across multiple Steps)
async function processDataTemplate(
  input: any,
  ctx: FlowContext,
  hooks: {
    validate?: (data: any) => Promise<boolean>
    transform?: (data: any) => Promise<any>
    save?: (data: any) => Promise<void>
  }
) {
  ctx.logger.info('Starting data processing template')

  // Step 1: Validation (customizable)
  const isValid = hooks.validate
    ? await hooks.validate(input)
    : await defaultValidate(input)

  if (!isValid) {
    throw new Error('Validation failed')
  }

  // Step 2: Transform (customizable)
  const transformed = hooks.transform
    ? await hooks.transform(input)
    : await defaultTransform(input)

  // Step 3: Save (customizable)
  if (hooks.save) {
    await hooks.save(transformed)
  } else {
    await defaultSave(transformed, ctx)
  }

  ctx.logger.info('Data processing completed')
  return transformed
}

// Step 1: Uses template with custom validation
export const config1: EventConfig = {
  type: 'event',
  name: 'ProcessUserData',
  subscribes: ['user.data.received']
}

export const handler1 = async (input, ctx) => {
  return processDataTemplate(input, ctx, {
    validate: async (data) => {
      // Custom validation for user data
      return data.email && data.name
    },
    transform: async (data) => {
      // Custom transformation
      return {
        ...data,
        email: data.email.toLowerCase(),
        createdAt: Date.now()
      }
    }
  })
}

// Step 2: Uses same template with different customization
export const config2: EventConfig = {
  type: 'event',
  name: 'ProcessProductData',
  subscribes: ['product.data.received']
}

export const handler2 = async (input, ctx) => {
  return processDataTemplate(input, ctx, {
    validate: async (data) => {
      // Custom validation for product data
      return data.sku && data.price > 0
    },
    transform: async (data) => {
      // Custom transformation
      return {
        ...data,
        sku: data.sku.toUpperCase(),
        price: Math.round(data.price * 100) / 100
      }
    }
  })
}
```

## Code Structure - Middleware Template (API)

```typescript
// Template middleware chain
const apiTemplate = [
  loggingMiddleware,    // Fixed
  authMiddleware,       // Fixed
  rateLimitMiddleware,  // Fixed
  // Custom middleware here
  validationMiddleware  // Fixed
]

export const config: ApiRouteConfig = {
  type: 'api',
  name: 'CreateResource',
  path: '/resources',
  method: 'POST',
  middleware: [
    ...apiTemplate,
    // Custom step: authorization
    async (req, ctx, next) => {
      const user = req.context.user
      if (!user.canCreateResource) {
        return { status: 403, body: { error: 'Forbidden' } }
      }
      return next()
    }
  ]
}
```

## Best Practices

1. **Extract Common Logic**: Винеси повторювані частини в template
2. **Provide Hooks**: Дай можливість кастомізувати ключові кроки
3. **Default Implementation**: Забезпеч default для всіх hooks
4. **Documentation**: Документуй які hooks доступні
5. **Testing**: Тестуй template з різними hooks

## Common Mistakes

❌ **Too rigid** - немає достатньо hooks
❌ **Too flexible** - занадто багато варіацій
❌ **Missing defaults** для optional hooks
❌ **Poor naming** hooks
❌ **No validation** hook implementations

## Use Cases

- **Data Processing Pipeline**: Validate → Transform → Save
- **API Request Handling**: Log → Auth → Validate → Process → Response
- **Email Sending**: Prepare → Format → Send → Log
- **Report Generation**: Gather Data → Format → Generate → Distribute
- **Webhook Processing**: Verify → Parse → Process → Respond

## Example: Report Generation Template

```typescript
// Report generation template
interface ReportHooks {
  gatherData: (params: any) => Promise<any>
  formatData?: (data: any) => Promise<any>
  generateReport?: (data: any) => Promise<Buffer>
  distribute?: (report: Buffer) => Promise<void>
}

async function generateReportTemplate(
  params: any,
  ctx: FlowContext,
  hooks: ReportHooks
): Promise<string> {
  ctx.logger.info('Starting report generation', { params })

  // Step 1: Gather data (required, custom)
  const rawData = await hooks.gatherData(params)
  await ctx.state.set(ctx.traceId, 'rawData', rawData)

  // Step 2: Format data (optional, custom)
  const formattedData = hooks.formatData
    ? await hooks.formatData(rawData)
    : await defaultFormatData(rawData)

  await ctx.state.set(ctx.traceId, 'formattedData', formattedData)

  // Step 3: Generate report (optional, custom)
  const report = hooks.generateReport
    ? await hooks.generateReport(formattedData)
    : await defaultGeneratePDF(formattedData)

  // Step 4: Save report
  const reportId = `report_${Date.now()}`
  await ctx.state.set(reportId, 'content', report)

  // Step 5: Distribute (optional, custom)
  if (hooks.distribute) {
    await hooks.distribute(report)
  } else {
    await defaultEmailReport(report, params.email)
  }

  ctx.logger.info('Report generation completed', { reportId })
  return reportId
}

// Sales Report - uses template
export const salesReportConfig: EventConfig = {
  type: 'event',
  name: 'GenerateSalesReport',
  subscribes: ['report.sales.requested'],
  emits: ['report.generated']
}

export const salesReportHandler = async (input, ctx) => {
  const reportId = await generateReportTemplate(input, ctx, {
    gatherData: async (params) => {
      // Custom: gather sales data
      ctx.logger.info('Gathering sales data', { params })
      return await fetchSalesData(params.dateRange)
    },
    formatData: async (data) => {
      // Custom: format for sales report
      return {
        summary: calculateSummary(data),
        details: data,
        charts: generateCharts(data)
      }
    },
    distribute: async (report) => {
      // Custom: send to multiple recipients
      await sendToSlack(report)
      await sendEmail(report, input.recipients)
    }
  })

  await ctx.emit({
    topic: 'report.generated',
    data: { reportId, type: 'sales' }
  })
}

// Inventory Report - uses same template differently
export const inventoryReportConfig: EventConfig = {
  type: 'event',
  name: 'GenerateInventoryReport',
  subscribes: ['report.inventory.requested'],
  emits: ['report.generated']
}

export const inventoryReportHandler = async (input, ctx) => {
  const reportId = await generateReportTemplate(input, ctx, {
    gatherData: async (params) => {
      // Custom: gather inventory data
      ctx.logger.info('Gathering inventory data')
      return await fetchInventoryData()
    },
    formatData: async (data) => {
      // Custom: format for inventory report
      return {
        lowStock: data.filter(item => item.quantity < 10),
        outOfStock: data.filter(item => item.quantity === 0),
        all: data
      }
    }
    // Uses default PDF generation and email distribution
  })

  await ctx.emit({
    topic: 'report.generated',
    data: { reportId, type: 'inventory' }
  })
}

// Default implementations
async function defaultFormatData(data: any) {
  return {
    timestamp: Date.now(),
    data
  }
}

async function defaultGeneratePDF(data: any): Promise<Buffer> {
  // Generate simple PDF
  return Buffer.from(JSON.stringify(data, null, 2))
}

async function defaultEmailReport(report: Buffer, email: string) {
  await sendEmail({
    to: email,
    subject: 'Your Report',
    attachments: [
      { filename: 'report.pdf', content: report }
    ]
  })
}
```

## Testing

```bash
# Test sales report
npx motia emit --topic "report.sales.requested" --message '{
  "dateRange": {
    "start": "2025-01-01",
    "end": "2025-01-31"
  },
  "recipients": ["manager@company.com"]
}'

# Test inventory report
npx motia emit --topic "report.inventory.requested" --message '{
  "email": "admin@company.com"
}'

# Check generated reports
npx motia state get "report_*" "content"
```

## Template with Configuration

```typescript
// Configuration-driven template
interface ProcessingConfig {
  validationRules: string[]
  transformations: string[]
  outputFormat: 'json' | 'xml' | 'csv'
}

async function configDrivenTemplate(
  input: any,
  config: ProcessingConfig,
  ctx: FlowContext
) {
  // Validation based on config
  for (const rule of config.validationRules) {
    await applyValidationRule(input, rule)
  }

  // Transformations based on config
  let data = input
  for (const transformation of config.transformations) {
    data = await applyTransformation(data, transformation)
  }

  // Output format based on config
  switch (config.outputFormat) {
    case 'json':
      return JSON.stringify(data)
    case 'xml':
      return convertToXML(data)
    case 'csv':
      return convertToCSV(data)
  }
}

// Usage
export const handler = async (input, ctx) => {
  const config: ProcessingConfig = {
    validationRules: ['required', 'email'],
    transformations: ['lowercase', 'trim'],
    outputFormat: 'json'
  }

  return configDrivenTemplate(input, config, ctx)
}
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: Any (utility pattern)
**Complexity**: ⭐⭐⭐☆☆ (Medium)
**Use Frequency**: ⭐⭐⭐☆☆ (Medium)
